from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Session

Base = declarative_base()


class Entity(Base):
    __tablename__ = 'entity'
    handle = Column(String, primary_key=True)
    name = Column(String)
    layer = Column(String)
    document = Column(String)
    layer_obj = relationship(
        'Layer',
        primaryjoin="and_(Entity.document==Layer.document," "Entity.layer==Layer.name)",
    )


class Layer(Base):
    __tablename__ = 'layer'
    handle = Column(String, primary_key=True)
    name = Column(String, ForeignKey('entity.layer'), primary_key=True)
    document = Column(String, ForeignKey('entity.document'), primary_key=True)


if __name__ == '__main__':
    engine = create_engine('sqlite:///test2.db', echo=True)
    Base.metadata.create_all(engine)

    session = Session(engine)

    layer1 = Layer(handle='asdf1234', name='G-ANNO', document='ABCM01.dwg')
    layer2 = Layer(handle='asdf7890', name='G-ASDF', document='ABCM01.dwg')
    session.add(layer1)
    session.add(layer2)
    session.commit()

    entity1 = Entity(handle='fdsa432', name='circle', layer='G-ANNO', document='ABCM01.dwg')
    entity2 = Entity(handle='fdsaa543', name='circle', layer='B-ANNO', document='ABCM01.dwg')
    session.add(entity1)
    session.add(entity2)
    session.commit()

    session.close()