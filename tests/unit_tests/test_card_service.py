from credcrud.card.models import Card
from credcrud.card.repositories import CardRepository
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
