from unittest import mock

import psycopg2
import pytest

from credcrud.card.schemas import CardPayload
from credcrud.database import DATABASE_CREDENTIALS, DATABASE_NAME


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
            "cvv": "1234",
            **kwargs
        }

    return _builder


@pytest.fixture()
def build_card_payload():
    def _builder(**kwargs):
        return CardPayload(**{
            "number": "5425233430109903",
            "holder": "Jonhnatha Trigueiro",
            "exp_date": "02/2026",
            "cvv": "1234",
            **kwargs
        })

    return _builder

@pytest.fixture()
def rsa_private_key_as_text_1024():
    return """-----BEGIN ENCRYPTED PRIVATE KEY-----
MIIC3TBXBgkqhkiG9w0BBQ0wSjApBgkqhkiG9w0BBQwwHAQIZ5cpcyEN+ZMCAggA
MAwGCCqGSIb3DQIJBQAwHQYJYIZIAWUDBAEqBBBPKy4jixm4WpUrvPJxvRQbBIIC
gFwCSbC1V0hOXKr4HwJOrio9cMsB67stk8+TAifMLmpbana8nnR/VXK45uYs2jKd
l/Qjk/nOqKBIoy/UQwhZNAaSQ5bcYLLBWg90EQFNG7ev6o6QlHrpOrtmgvrJ3kYQ
5LUk7xoCaxb7j3IbwhsqGtUSuhJNmxD46IyFTOejBfAU2V2r8/IsTK8s4irvi5zt
hrN099/512UYsXwpW/3MW0xSuovL7ekyuGPWXcfftkts9BZj/bD7b5/z9QA4YlOD
oViOJBy+i+jQbtPA7a889jh4SXfyiDyuZgO9S9upO3euTdo5lZLivM/5xKljY3J7
jHz+fjuGkhBKXddanVFT31Yw/FzCehKnJQuTZSyAQBi8/e2jH7pjlaRucLjaeknf
WNsSu2zE+Lux7lujIwhDwNfz9AWoZE9w30IAjLuB7bPJNkc4CIoYHQf6xlFSb4eR
deEY7bK+FgjslbO6gfZkweTEGleI8Q44OC2XZxUXGZFNQfm2xK1FOjsG1zlE0ETm
Cy7X79xg47M7ZwXkzcL7JNAV1EZ27eM/DLpzyea4jil81N4W53qA1lUP2jrNy/LP
ozYOAgET5VFJpIj5tZjNew+72hPPjbos0EX+VuczkzQAjl09C0n1uZ7u1FKsDKiY
ApXuvCjmU+ZnZKKxcvF47JU4N8FTrs3EpOoIw/BZp10rz0DD4en/ZxLfGquxmcWd
NcK7tJRg5bjWm17WIvPfgsyN7aycPB4/vNkrDaYm2P4e/XFVWrWidcnT0UXIBHjW
ctAUjkOd1Sj/dEAPeHmwWtW2vJJcHNdq4BFN21WXQHy+1KEwjnnd4zCNSHu+O6K1
uwQ/53D0EhGF5r7anNKUiHQ=
-----END ENCRYPTED PRIVATE KEY-----"""

@pytest.fixture()
def rsa_text_decrypted_example():
    return "UM TEXTO TESTE SECRETO PARA CRIPTOGRAFIA"


@pytest.fixture()
def rsa_text_encrypted_example():
    return ("Sq3GPz6DrWtt0o6OcXSnIaspNHVevbUZ9fdKDhLFu1AMFHYOrUx0wwO+fJKGRLYggMRnM1K6+jOozTe1CIVmz8+cM3w7LyOywtksw"
            "Y4bu13QTeLXPR1Yhf9sz9P9JamHI9FQq1RQDEesA81jmxSj0PIys5X9qOTL3/azAsStFpQ=")

@pytest.fixture(autouse=True)
def patch_open_file(rsa_private_key_as_text_1024):
    with mock.patch("builtins.open", mock.mock_open(read_data=rsa_private_key_as_text_1024)), mock.patch("os.path.isfile", return_value=True):
        yield
