from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from credcrud.database import DATABASE_URL, Base


@contextmanager
def test_db_session():
    engine = create_engine(f"{DATABASE_URL}_test")

    Base.metadata.create_all(bind=engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        yield session
    finally:
        session.close()
        engine.dispose()
