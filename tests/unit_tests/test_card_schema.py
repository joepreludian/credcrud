import pytest
import datetime
from pydantic import ValidationError

from credcrud.card.schemas import Card, CardPayload
from credcrud.card.models import Card as CardModel


class TestCardSchema:
    def test_process_payload(self, build_card_payload):
        payload = build_card_payload()
        card = Card.from_payload(payload)

        assert type(card) is Card
        assert card.card_holder == payload.holder
        assert card.card_number == payload.number
        assert card.cvv == payload.cvv

    def test_payload_to_model(self, build_card_payload):
        payload = build_card_payload()
        card = Card.from_payload(payload)

        card_model = card.to_model()

        assert type(card_model) is CardModel
        assert card_model.card_number == payload.number
        assert card_model.card_holder == payload.holder
        assert card_model.cvv == payload.cvv
        assert type(card_model.expiration_date) is datetime.date

    @pytest.mark.parametrize(
        ("override", "error_message"),
        (
            ({'number': '1234'}, "Card number must have 16 digits"),
            ({'number': '1234abc'}, "Card number must have only numbers"),
            ({'exp_date': '01/12/1993'}, "Card exp_date must be on mm/YYYY format"),
            ({'cvv': '1abc'}, "CVV must be a number with 3 up to 4 digits"),
        )
    )
    def test_payload_invalid(self, override, error_message, build_card_payload):
        payload = build_card_payload(**override)
        with pytest.raises(ValidationError) as exception_raised:
            Card.from_payload(payload)

        assert error_message in str(exception_raised)

    def test_payload_to_representation(self, build_card_payload):
        payload = build_card_payload()
        card = Card.from_payload(payload)

        output = card.to_representation()

        assert type(output) is CardPayload
        assert output.number == f"************{payload.number[12:]}"
        assert output.exp_date == payload.exp_date
