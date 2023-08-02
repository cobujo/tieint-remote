from typing import Optional
from settings import auto_config as cfg
from sqlalchemy.orm.decl_api import DeclarativeMeta
from sqlalchemy.sql import text
from sqlalchemy.exc import IntegrityError
from mylogger import logger
from typing import Optional
from sqlalchemy.engine.base import Engine
from collections import namedtuple


def db_add_or_merge(instance, session_scope, return_action=False) -> Optional[str]:
    """
    From kyo-fin-data
    add or merge, to avoid expcetions when data is already in the table
    :param instance:
        SQLAclhemy object instance
    :param session_scope:
        run function inside initialized session scope
    :param return_action: boolean
        if true, return if the object was added or merged with existing object
        *not always reliable
    :return:
    """
    try:
        instance = session_scope.merge(instance)
        action = 'updated'
    except IntegrityError:
        action = 'inserted'

    session_scope.add(instance)
    if return_action:
        return action
    return


def list_properties_from_class(cls) -> Optional[list]:
    """
    *** NOTE: by using vars, this is only getting properties from the class and nothing inherited (and we want it that way)!
     because both acad classes and sql models are inheriting what's needed from parents (sql -> __abstract__ = True)
    :param cls:
    :return:
    """
    class_vars = vars(cls)
    props = [p for p in class_vars if getattr(cls, p).__class__.__name__ == 'property']
    if not props:
        logger.error(f'no properties found in class: {cls.__name__}')
        return

    return props


sql_type_dict = {
    int: 'Column(INTEGER)',
    str: 'Column(TEXT)',
    float: 'Column(REAL)',
    bool: 'Column(BOOLEAN)',
    tuple: 'Column(MyTuple())'
}


# TODO: test, it appears list_properties_from_class uses the class, but guess_columns_from_instance uses an instance?
def guess_columns_from_instance(cls) -> Optional[str]:
    props = list_properties_from_class(cls)
    if not props:
        return

    codestring = ''
    for prop in props:
        try:
            attr = getattr(cls, prop)
            col_string = sql_type_dict.get(type(attr), '???')
        except AttributeError:
            col_string = 'AttrError?'

        codestring = codestring + f'{prop} = {col_string}\n'

    return codestring


def query_stmt(query) -> str:
    """
    If Local, will show compiled query, otherwise will show parametrized query
    :param query:
    :return:
    """
    if cfg.__name__ == 'Local':
        return query.statement.compile(compile_kwargs={"literal_binds": True})
    else:
        return str(query)


def custom_create(metadata, engine: Engine, view_statements: Optional[dict],
                  tables_views: Optional[list[DeclarativeMeta]] = None):
    """
    Modeled after function of the same name in kyo-fin-data
    :param metadata: Base.metadata
    :param engine: engine
        Specific SQLite engine created (initialized) previously
    :param view_statements: dict
        dictionary of view_name: stmt (same as kyo-fin-data)
    :param tables_views: list
        if not provided, will get and create all tables from metadata
    :return:
    """
    if not tables_views:
        tables_views = metadata.sorted_tables
    else:
        tables_views = [t.__table__ for t in tables_views]

    # NOTE: views must follow the prefix convention of v_ (unable to give custom attributes to table instances within metadata at this point...)
    tables = [t for t in tables_views if t.fullname[:2] != 'v_']
    views = [t for t in tables_views if t.fullname[:2] == 'v_']

    if tables:
        metadata.create_all(engine, tables=tables)
        logger.info(f'{len(tables)} table(s) pre-existing or created (assuming no errors)!')

    if views:
        if not view_statements:
            logger.error(f'You are trying to create views ({views}) but have not included any view_statements arg!')
            return

        with engine.begin() as conn:
            for view in views:
                view_name = view.fullname
                try:
                    stmt = view_statements[view_name]
                except KeyError:
                    logger.error(f'You have not defined a select statement for view: {view_name}')

                view_stmt = f'CREATE OR REPLACE VIEW {view_name} AS {stmt}'
                sql = text(view_stmt)
                conn.execute(sql)

            conn.close()

        logger.info(f'{len(views)} view(s) created (assuming no errors)!')


def field_names_from_raw_sql(stmt: str) -> Optional[list]:
    if stmt[:7].upper() != 'SELECT ':
        raise ValueError(f'Expecting statement to begin with SELECT, instead is: {stmt[:6]}')

    if 'FROM' not in stmt.upper():
        raise ValueError('Expecting FROM to be in statement (getting fields between SELECT and FROM), not found!')

    from_find = stmt.upper().find('FROM')
    field_text = stmt[7:from_find]

    field_split = field_text.split(',')
    field_names = [f.strip() for f in field_split]

    return field_names


def ss_result_to_namedtuples(result, sql_model, tuple_name: str = None) -> Optional[list]:
    """
    Use this function when needing to store results in an organized way (namedtuples)
    for use outside the session scope
    :param result:
    :param sql_model:
    :param tuple_name: str
        if None, will create name from sql_model.__name__
    :return: list
        list of namedtuples
    """
    try:
        cols = sql_model.__table__.columns.keys()
    except AttributeError:
        logger.error(f'unable to determine columns from object, object type: {type(sql_model)}')
        return

    if not tuple_name:
        tuple_name = sql_model.__name__.replace('Base', '')

    res_list = []
    for row in result:
        Ntuple = namedtuple(tuple_name, cols)
        row_ntuple = Ntuple(*[getattr(row, field) for field in cols])
        res_list.append(row_ntuple)

    return res_list
