from sqlalchemy import ForeignKey, create_engine, Column, Integer, CheckConstraint
from sqlalchemy import String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
import logging
from sqlalchemy import inspect
# from setup import Base, engine

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

Base = declarative_base()

# Credentials for connecting to mysql db
# USERNAME = "botontapwater"
# PASSWORD = "TwoGreen1."
# HOST = "localhost"
# DB = "karibunami"

USERNAME = "ray"
PASSWORD = "raypassword"
HOST = "localhost"
DB = "karibunami"

SQLALCHEMY_DATABASE_URI = f'mysql+mysqlconnector://{USERNAME}:{PASSWORD}@{HOST}/{DB}'

# Create engine
engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)

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

# Check if the "bookmarks" table exists
inspector = inspect(engine)

if "places" not in inspector.get_table_names():
    print("places table doesn't exist, creating it!")
    Base.metadata.create_all(engine)
else:
    print("places table already exists! Skipping")