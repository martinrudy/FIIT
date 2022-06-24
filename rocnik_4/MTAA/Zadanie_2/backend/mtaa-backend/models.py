from xmlrpc.client import Boolean
from sqlalchemy import Table, Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    password = Column(String(50))
    email = Column(String(120), unique=True)
    fridges = relationship("Fridge")

    def __init__(self, name=None, email=None, password=None):
        self.name = name
        self.email = email
        self.password = password

    def __repr__(self):
        return f"<User {self.name!r} {self.email}>"

fridge_items = Table('fridge_items', Base.metadata,
    Column('fridge_id', ForeignKey('fridges.id'), primary_key=True),
    Column('item_id', ForeignKey('items.id'), primary_key=True),
    Column('item_count', Integer)
)

class Fridge(Base):
    __tablename__ = "fridges"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String(50), nullable = False)
    item = relationship("Item", secondary=fridge_items)
    in_use = Column(Boolean, nullable = False)


    def __init__(self, name=None, user_id=None, in_use=None):
        self.name = name
        self.user_id = user_id
        self.in_use = in_use

    def __repr__(self):
        return f"<Fridge {self.name!r}>"

recipe_items = Table('recipe_items', Base.metadata,
    Column('recipe_id', ForeignKey('recipes.id'), primary_key=True),
    Column('item_id', ForeignKey('items.id'), primary_key=True),
    Column('item_count', Integer)
)

class Recipe(Base):
    __tablename__ = "recipes"
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable = False)
    text = Column(String(1000), nullable = False)
    item = relationship("Item", secondary=recipe_items)


    def __init__(self, title=None, text=None):
        self.title = title
        self.text = text

    def __repr__(self):
        return f"<Item {self.title!r}>"

class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable = False)
    category = Column(String(50), nullable = False)
    file_path = Column(String(200), nullable = False)


    def __init__(self, title=None, category=None, file_path=None):
        self.title = title
        self.category = category
        self.file_path = file_path

    def __repr__(self):
        return f"<Item {self.title!r}>"

