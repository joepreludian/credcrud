import os
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_CREDENTIALS = os.environ.get("DATABASE_CREDENTIALS")
DATABASE_NAME = os.environ.get("DATABASE_NAME")

DATABASE_URL = f"{DATABASE_CREDENTIALS}/{DATABASE_NAME}"

Base = declarative_base()
Engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autoflush=False, bind=Engine, autocommit=False)


@contextmanager
def db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
