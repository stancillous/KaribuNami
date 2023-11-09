from sqlalchemy import ForeignKey, create_engine, Column, Integer
from sqlalchemy import String, Boolean
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
import logging
from sqlalchemy import inspect
# from server.tables.setup import Base, engine

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

Base = declarative_base()

class User(Base):
    """Table users"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    username = Column(String(256), nullable=False)
    password = Column(String(256), nullable=False)
    email = Column(String(256), nullable=False)
    verification_link = Column(String(256), nullable=False)
    email_verified = Column(Boolean, nullable=False, default=False)
