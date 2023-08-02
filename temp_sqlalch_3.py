from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()


class ObjParent(Base):
    __tablename__ = 'objs_parent'
    id_ = Column(Integer, primary_key=True)
    tablename_ = Column(String)

    coordinates = relationship("Coordinate", back_populates="obj")
    # Add common properties for all entity classes here
    __mapper_args__ = {
        'polymorphic_identity': __tablename__,
        'polymorphic_on': tablename_
    }


class Obj(ObjParent):
    __abstract__ = True
    id_ = Column(Integer, ForeignKey('objs_parent.id_'), primary_key=True)
    handle = Column(String, primary_key=True)
    document = Column(String, primary_key=True)


class Entity(Obj):
    __abstract__ = True
    layer = Column(String)


class Block(Entity):
    __tablename__ = 'blocks'
    # handle = Column(String, ForeignKey('objs.handle'), primary_key=True)
    name = Column(String)

    __mapper_args__ = {
        'polymorphic_identity': __tablename__,
    }


class Text(Entity):
    __tablename__ = 'texts'
    # handle = Column(String, ForeignKey('objs.handle'), primary_key=True)
    content = Column(String)

    __mapper_args__ = {
        'polymorphic_identity': __tablename__
    }


class Coordinate(Base):
    __tablename__ = 'coordinates'
    id = Column(Integer, primary_key=True)
    xyz = Column(String)
    obj_id = Column(String, ForeignKey('objs_parent.id_'))
    obj = relationship("ObjParent", back_populates="coordinates")


def test():
    # Create the database and tables
    engine = create_engine('sqlite:///my_database.db')
    Base.metadata.create_all(engine)

    # Create a session to interact with the database
    Session = sessionmaker(bind=engine)
    session = Session()

    # Create a new Block instance
    new_block = Block(handle='a1', name='tblock', document='abc123.dwg')

    # Add the Block instance to the session
    session.add(new_block)

    # Create a new Coordinate instance and relate it to the new_block instance
    new_coordinate = Coordinate(obj=new_block, xyz='1, 2, 3')

    # Add the Coordinate instance to the session
    session.add(new_coordinate)

    new_text = Text(handle='b2', content='this is my text', document='abc123.dwg')
    text_coords = Coordinate(obj=new_text, xyz='0, 0, 0')

    session.add(new_text)
    session.add(text_coords)

    # Commit the changes to the database
    session.commit()

    # Close the session
    session.close()


def create_sess():
    engine = create_engine('sqlite:///my_database.db')

    Session = sessionmaker(bind=engine)
    return Session()
