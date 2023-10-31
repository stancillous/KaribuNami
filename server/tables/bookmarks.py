from sqlalchemy import ForeignKey, create_engine, Column, Integer, CheckConstraint
from sqlalchemy import String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
import logging
from sqlalchemy import inspect
# from server.tables.setup import Base, engine
from server.tables.users import User
from server.tables.places import Place

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

Base = declarative_base()

class Bookmark(Base):
    """Table bookmarks"""
    __tablename__ = "bookmarks"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    place_id = Column(String(256), ForeignKey(Place.google_api_place_id), nullable=False)
    bookmarked = Column(Integer, nullable=False)

    __table_args__ = (CheckConstraint('bookmarked IN (0, 1)', name='check_bookmarked'),)