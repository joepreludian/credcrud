import uuid

import pytest

from credcrud.card.exceptions import CardNotFoundException
from credcrud.card.schemas import Card as CardSchema
from credcrud.card.services import CardService
from tests.builders import test_db_session
from types import GeneratorType


class TestCardService:

    def setup(self):
        self.card_svc = CardService(db_session=test_db_session)

    def test_create_card(self, build_card_payload):
        card_payload = build_card_payload()

        new_card = self.card_svc.create(card_payload)

        assert type(new_card) is CardSchema
        assert new_card.to_representation().exp_date == card_payload.exp_date
        assert new_card.id is not None

    def test_get_card_by_id(self, build_card_payload):

        card_payload = build_card_payload(number="374245455400126")
        created_card = self.card_svc.create(card_payload)
        card_found = self.card_svc.get_by_id(created_card.id)

        for attribute in ['id', 'card_number', 'card_holder', 'expiration_date', 'cvv']:
            assert getattr(created_card, attribute) == getattr(card_found, attribute)

    def test_get_card_by_id_not_found(self):

        with pytest.raises(CardNotFoundException):
            self.card_svc.get_by_id(id=str(uuid.uuid4()))

    def test_get_all_cards(self):
        all_cards = self.card_svc.get_all()

        assert type(all_cards) is GeneratorType
        assert type(next(all_cards)) is CardSchema
