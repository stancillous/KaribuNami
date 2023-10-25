from sqlalchemy import ForeignKey, create_engine, Column, Integer
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
USERNAME = "botontapwater"
PASSWORD = "TwoGreen1."
HOST = "localhost"
DB = "karibunami"

SQLALCHEMY_DATABASE_URI = f'mysql+mysqlconnector://{USERNAME}:{PASSWORD}@{HOST}/{DB}'

# Create engine
engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)

class User(Base):
    """Table users"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    username = Column(String(256), nullable=False)
    password = Column(String(256), nullable=False)

# Check if the "users" table exists
inspector = inspect(engine)
if "users" not in inspector.get_table_names():
    print("Users table doesn't exist, creating it!")
    Base.metadata.create_all(engine)
else:
    print("Users table already exist, skip it!")