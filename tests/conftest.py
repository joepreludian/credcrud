import pytest
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from credcrud.database import Base, DATABASE_CREDENTIALS, DATABASE_NAME, DATABASE_URL
from contextlib import contextmanager


@pytest.fixture(autouse=True, scope="session")
def setup_test_database():
    db_name = f"{DATABASE_NAME}_test"

    def _connect():
        superuser_conn = psycopg2.connect(DATABASE_CREDENTIALS)
        superuser_conn.autocommit = True
        superuser_cursor = superuser_conn.cursor()

        return superuser_conn, superuser_cursor

    conn, cursor = _connect()
    try:
        cursor.execute(f"DROP DATABASE IF EXISTS {db_name}")
        cursor.execute(f"CREATE DATABASE {db_name}")
    finally:
        cursor.close()
        conn.close()

    yield

    conn, cursor = _connect()
    try:
        cursor.execute(f"DROP DATABASE {db_name}")
    finally:
        cursor.close()
        conn.close()
