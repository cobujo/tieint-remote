from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref, declared_attr, declarative_base, sessionmaker

Base = declarative_base()


class Entity(Base):
    __abstract__ = True
    handle = Column(String, primary_key=True)
    document = Column(String)

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    @declared_attr
    def coordinates(cls):
        return relationship(
            "Coordinate",
            primaryjoin="and_(Coordinate.entity_handle=={}.__table__.c.handle, "
                        "Coordinate.entity_type=='{}')".format(cls.__name__, cls.__name__),
            backref=backref("parent_{}".format(cls.__name__.lower()), uselist=False)
        )


class Block(Entity):
    __tablename__ = 'blocks'
    name = Column(String)
    layer = Column(String)


class Text(Entity):
    __tablename__ = 'texts'
    content = Column(String)
    style = Column(String)
    layer = Column(String)


class Coordinate(Base):
    __tablename__ = 'coordinate'
    id = Column(Integer, primary_key=True)
    entity_handle = Column(String, ForeignKey('entity.handle'))
    entity_type = Column(String)
    xyz = Column(String)
    space = Column(String)


def test():
    # Create the database and tables
    engine = create_engine('sqlite:///my_database.db')
    Base.metadata.create_all(engine)

    # Create a session to interact with the database
    Session = sessionmaker(bind=engine)
    session = Session()

    new_block = Block(handle='a1', document='abc123.dwg', name='tblock', layer='gg')
    session.add(new_block)

    new_text = Text(handle='b2', document='abc123.dwg', content='this is the content', style='subtitle', layer='anno')
    session.add(new_text)

    new_coordinate = Coordinate(entity_handle='a1', entity_type='')