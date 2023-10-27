from sqlalchemy import ForeignKey, create_engine, Column, Integer, CheckConstraint
from sqlalchemy import String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
import logging
from sqlalchemy import inspect

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

Base = declarative_base()


class Place(Base):
    """Table places"""
    __tablename__ = "places"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(256), nullable=False)
    rating = Column(String(256), nullable=False)
    open_now = Column(String(256), nullable=True)
    mobile_number = Column(String(256), nullable=True)
    location = Column(String(256), nullable=False)
    photos = Column(String(256), nullable=True)
    reviews = Column(String(256), nullable=True)
