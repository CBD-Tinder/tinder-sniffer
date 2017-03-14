import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = Column(String(24), primary_key=True)
    age = Column(Integer, nullable=False)
    gender = Column(Integer, nullable=False)
    name = Column(String(50), nullable=False)

class Photo(Base):
    __tablename__ = 'photo'

    id = Column(Integer, primary_key=True)
    url = Column(String(255), nullable=False)
    user_id = Column(String(24), ForeignKey('user.id'))
    user = relationship(User)

class Position(Base):
    __tablename__ = 'position'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(String(24), ForeignKey('user.id'))
    user = relationship(User)
    lat = Column(Float, nullable=False)
    lon = Column(Float, nullable=False)

def init_database(db_name):
    engine = create_engine(db_name)
    Base.metadata.create_all(engine)
