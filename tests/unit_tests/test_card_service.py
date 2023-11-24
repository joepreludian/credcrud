import uuid

import pytest
from credcrud.card.schemas import Card as CardSchema
from credcrud.card.models import Card
from credcrud.card.repositories import CardRepository
from tests.builders import test_db_session

from datetime import datetime, timedelta


@pytest.fixture()
def dummy_card():
    def _builder(**kwargs):
        return {
            "card_number": "0000111122223333",
            "card_holder": "Jonhnatha Trigueiro",
            "expiration_date": datetime.now() + timedelta(days=5),
            "cvv": "1234",
            **kwargs
        }

    return _builder

class TestCardService:
    def test_create_card(self, dummy_card):

        dummy = dummy_card(card_holder="Jessica Ribeiro")

        cr = CardRepository(test_db_session)
        created_card = cr.create(
            Card(
                card_number=card_number,
                card_holder=card_holder,
                expiration_date=expiration_date,
                cvv=cvv
            )
        )

        assert created_card.id is not None
        assert created_card.card_number == card_number
        assert created_card.card_holder == card_holder
        assert created_card.expiration_date == expiration_date
        assert created_card.cvv == cvv

