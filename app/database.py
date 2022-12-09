from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from os import getenv
from dotenv import load_dotenv

load_dotenv()
HOST = getenv("host")
USER = getenv("user")
PASSWORD = getenv("password")
DBNAME = getenv("database")
URL = f"postgresql://{USER}:{PASSWORD}@{HOST}/{DBNAME}"

engine = create_engine(URL)
Session_Local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = Session_Local()
    try:
        yield db
    finally:
        db.close()
