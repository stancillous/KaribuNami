from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

Base = declarative_base()

# Credentials for connecting to mysql db
USERNAME = "ray"
PASSWORD = "raypassword"
HOST = "localhost"
DB = "karibunami"
# USERNAME = "botontapwater"
# PASSWORD = "TwoGreen1."
# HOST = "localhost"
# DB = "karibunami"

SQLALCHEMY_DATABASE_URI = f'mysql+mysqlconnector://{USERNAME}:{PASSWORD}@{HOST}/{DB}'

# Create engine
engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)

# Create tables
