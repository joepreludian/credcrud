import uuid

import pytest

from credcrud.card.models import Card
from credcrud.card.repositories import CardRepository
from credcrud.card.exceptions import CardNotFoundException
from tests.builders import test_db_session


class TestCardRepository:
    def test_create_card(self, build_card_data):
        card_data = build_card_data(card_holder="Jessica Ribeiro")

        cr = CardRepository(test_db_session)
        created_card = cr.create(
            Card(
                card_number=card_data["card_number"],
                card_holder=card_data["card_holder"],
                expiration_date=card_data["expiration_date"],
                cvv=card_data["cvv"]
            )
        )

        assert created_card.id is not None
        assert created_card.card_number == card_data["card_number"]
        assert created_card.card_holder == card_data["card_holder"]
        assert created_card.expiration_date == card_data["expiration_date"]
        assert created_card.cvv == card_data["cvv"]

        cr.delete(created_card)

    def test_fetch_card(self, build_card_data):
        card_data = build_card_data(card_number="1000111122223333")

        cr = CardRepository(test_db_session)
        created_card = cr.create(
            Card(
                card_number=card_data["card_number"],
                card_holder=card_data["card_holder"],
                expiration_date=card_data["expiration_date"],
                cvv=card_data["cvv"]
            )
        )

        retrieved_card = cr.get_by_id(created_card.id)

        assert type(retrieved_card) is Card

        for attribute in ("card_number", "card_holder", "expiration_date", "cvv", "id"):
            assert getattr(retrieved_card, attribute) == getattr(created_card, attribute)

        cr.delete(retrieved_card)
    def test_fetch_card_not_found(self):
        cr = CardRepository(test_db_session)

        search_id = str(uuid.uuid4())
        with pytest.raises(CardNotFoundException) as exc:
            card = cr.get_by_id(id=search_id)

        assert f"The Card {search_id} could not be found" in str(exc)

    def test_get_all_cards(self, build_card_data):
        card_data = build_card_data(card_number="6062826786276634")

        cr = CardRepository(test_db_session)

        created_card = cr.create(
            Card(
                card_number=card_data["card_number"],
                card_holder=card_data["card_holder"],
                expiration_date=card_data["expiration_date"],
                cvv=card_data["cvv"]
            )
        )

        all_items = cr.get_all()

        assert type(all_items) is list
        assert len(all_items) > 0
        assert type(all_items[0]) is Card
