from sqlalchemy import ForeignKey, create_engine, Column, Integer, CheckConstraint
from sqlalchemy import String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
import logging
from sqlalchemy import inspect
from server.tables.users import User
from server.tables.places import Place

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

class Bookmark(Base):
    """Table bookmarks"""
    __tablename__ = "bookmarks"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    place_id = Column(Integer, ForeignKey(Place.id), nullable=False)
    bookmarked = Column(Integer, nullable=False)

    __table_args__ = (CheckConstraint('bookmarked IN (0, 1)', name='check_bookmarked'),)



# Check if the "bookmarks" table exists
inspector = inspect(engine)

if "bookmarks" not in inspector.get_table_names():
    print("bookmarks table doesn't exist, creating it!")
    Base.metadata.create_all(engine)
else:
    print("bookmarks table already exists! Skipping")