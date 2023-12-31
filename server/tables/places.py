from sqlalchemy import ForeignKey, create_engine, Column, Integer, CheckConstraint, DateTime
from sqlalchemy import String, Text
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
import logging
from sqlalchemy import inspect
from datetime import datetime

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

Base = declarative_base()


class Place(Base):
    """Table places"""
    __tablename__ = "places"

    google_api_place_id = Column(String(256), primary_key=True, nullable=False)
    name = Column(String(256), nullable=False)
    rating = Column(String(256), nullable=False)
    open_now = Column(String(256), nullable=True)
    mobile_number = Column(String(256), nullable=True)
    location = Column(String(256), nullable=False)
    photos = Column(Text, nullable=True)
    reviews = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    # type_of_place = Column(Text, nullable=True)
