from settings import auto_config as cfg
from sqlalchemy import create_engine
from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker
import os


# no db configs at this time, may add later (not sure what they would be for sqlite)

def safe_check_dot_db(db_name):
    """
    Using this in multiple places; add .db if not present, otherwise return the name
    :param db_name: str
    :return:
    """
    if db_name.endswith('.db'):
        return db_name

    no_ext = db_name.split('.')[0]
    return f'{no_ext}.db'


def engine_named(name: str):
    """
    Unlike other db instances, we'll want to input a name as we'll be dealing with different dbs under sqlite
    ONLY WORKS WITH SQLITE
    :param name: str
        probably the tool name-life_rev and a timestamp?
    :return:
    """
    db_filename = safe_check_dot_db(name)
    path_to_db = f'sqlite:///{os.path.join(cfg.DB_DIR, db_filename)}'
    return create_engine(path_to_db, echo=cfg.DB_ENGINE_ECHO)


@contextmanager
def session_scope(bind, autoflush=True, expire_on_commit=True):
    """
    https://docs.sqlalchemy.org/en/13/orm/session_basics.html#session-faq-whentocreate
    :param bind: engine
    :param autoflush: boolean
    :param expire_on_commit: boolean
    return:
    """
    Session = sessionmaker(bind=bind, autoflush=autoflush, expire_on_commit=expire_on_commit)
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
