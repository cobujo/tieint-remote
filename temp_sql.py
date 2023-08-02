from sql import session_scope, engine_named
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from sqlalchemy.orm import load_only
from sql.models import AcDbAttributeBase, AcadDocumentBase, AcDbBlockReferenceBase
from collections import namedtuple
from typing import Optional
from settings import constants as cn


def testsess():
    Session = sessionmaker(bind=engine_named('SNX406.db'))
    session = Session()
    return session


def test():
    with session_scope(engine_named('SNX402.db')) as ss:
        cols = AcDbBlockReferenceBase.__table__.columns.keys()
        result = ss.query(AcDbBlockReferenceBase).filter(AcDbBlockReferenceBase.name.like('i2436RD')).all()
        dba_list = []

        if result:
            for row in result:
                Asdf = namedtuple('Asdf', cols)
                dba = Asdf(*[getattr(row, field) for field in cols])
                dba_list.append(dba)

            #     print(row.handle, row.text_string)
            # DbAttributes = namedtuple(DbAttributes, cols_tuple)
            # dba_list = [DbAttributes(*[getattr(row, field) for field in cols_tuple]) for row in result]

    return dba_list


def other():
    with session_scope(engine_named('SNX406.db')) as ss:
        rev_strip_blocks_q = ss.query(AcDbBlockReferenceBase).filter(AcDbBlockReferenceBase.name.like('i2436RD')).all()
        for r in rev_strip_blocks_q:
            print(r.handle + ' -> ' + r.name)
