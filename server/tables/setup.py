from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# from sqlalchemy.orm import declarative_base
import os
from server.tables.users import User
from server.tables.places import Place
from server.tables.bookmarks import Bookmark
from sqlalchemy import inspect
from decouple import config

# Base = declarative_base()

# Credentials for connecting to mysql db
USERNAME = config("MYSQLUSERNAME")
PASSWORD = config("PASSWORD")
HOST = config("HOST")
DB = config("DB")

SQLALCHEMY_DATABASE_URI = f'mysql+mysqlconnector://{USERNAME}:{PASSWORD}@{HOST}/{DB}'

# Create engine
engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)

# Create tables
# Check if the "users" table exists
inspector = inspect(engine)
if "users" not in inspector.get_table_names():
    print("Users table doesn't exist, creating it!")
    User.__table__.create(bind=engine)
else:
    print("Users table already exist, Skipping!")

# Check if the "bookmarks" table exists
if "places" not in inspector.get_table_names():
    print("places table doesn't exist, creating it!")
    Place.__table__.create(bind=engine)
else:
    print("places table already exists! Skipping")

# Check if the "bookmarks" table exists
if "bookmarks" not in inspector.get_table_names():
    print("bookmarks table doesn't exist, creating it!")
    Bookmark.__table__.create(bind=engine)
else:
    print("bookmarks table already exists! Skipping")