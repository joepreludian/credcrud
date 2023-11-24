import os
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_CREDENTIALS = os.environ.get("DATABASE_CREDENTIALS")
DATABASE_NAME = os.environ.get("DATABASE_NAME")

DATABASE_URL = f"{DATABASE_CREDENTIALS}/{DATABASE_NAME}"

Base = declarative_base()
Engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autoflush=False, bind=Engine, autocommit=False)

@contextmanager
def database_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

