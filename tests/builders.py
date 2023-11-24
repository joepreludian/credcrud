import pytest
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from credcrud.database import Base, DATABASE_CREDENTIALS, DATABASE_NAME, DATABASE_URL
from contextlib import contextmanager


@contextmanager
def test_db_session():
    engine = create_engine(f"{DATABASE_URL}_test")

    Base.metadata.create_all(bind=engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    yield session

    session.close()
    engine.dispose()
