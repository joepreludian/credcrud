from datetime import datetime, timedelta
from credcrud.card.schemas import CardPayload

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


@pytest.fixture()
def build_card_data():
    def _builder(**kwargs):
        return {
            "card_number": "0000111122223333",
            "card_holder": "Jonhnatha Trigueiro",
            "exp_date": "02/2026",
            "expiration_date": datetime.now().date() + timedelta(days=5),
            "cvv": "1234",
            **kwargs
        }

    return _builder

@pytest.fixture()
def build_card_payload():
    def _builder(**kwargs):
        return CardPayload(**{
            "number": "0000111122223333",
            "holder": "Jonhnatha Trigueiro",
            "exp_date": "02/2026",
            "cvv": "1234",
            **kwargs
        })

    return _builder