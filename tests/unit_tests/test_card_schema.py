import datetime

import pytest
from pydantic import ValidationError

from credcrud.card.models import Card as CardModel
from credcrud.card.schemas import Card, RedactedCardPayload


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
            ({'number': '1234'}, "String should have at least 15 characters"),
            ({'number': '123456781234abcd'}, "Card number must have only numbers"),
            ({'number': '1111111111111111'}, "Card number provided is invalid"),
            ({'exp_date': '01/12/1993'}, "CardPayload must have expiration date in format mm/YYYY"),
            ({'exp_date': '09/2022'}, "Card has expired"),
            ({'cvv': '1abc'}, "CVV must be a number with 3 up to 4 digits"),
        )
    )
    def test_payload_invalid(self, override, error_message, build_card_payload):
        with pytest.raises(ValidationError) as exception_raised:
            payload = build_card_payload(**override)
            Card.from_payload(payload)

        assert error_message in str(exception_raised)

    @pytest.mark.parametrize(
        ("card_number", "brand"),
        (
                ("5425233430109903", "master"),
                ("4263982640269299", "visa"),
                ("6011000991300009", "discover"),
                ("374245455400126", "amex"),
                ("0000000000000000", None)
        )
    )
    def test_payload_to_representation(self, card_number, brand, build_card_payload):
        payload = build_card_payload(**{"number": card_number})
        card = Card.from_payload(payload)

        output = card.as_redacted_payload()

        assert type(output) is RedactedCardPayload
        assert output.number == f"************{payload.number[12:]}"
        assert output.exp_date == payload.exp_date
        assert output.brand == brand
