from datetime import date, datetime
from typing import Optional

from creditcard import CreditCard
from creditcard.exceptions import BrandNotFound
from pydantic import BaseModel, Field, model_validator

from credcrud.card.constants import CardConstants
from credcrud.card.models import Card as CardModel
from credcrud.card.utils import date_to_expire_date, expire_date_to_date


class CardPayload(BaseModel):
    exp_date: str
    holder: str
    number: str
    cvv: str

    @model_validator(mode="after")
    def validate(self):
        try:
            current_expiration_date = datetime.strptime(self.exp_date, "%m/%Y").date()
        except ValueError:
            raise ValueError("CardPayload must have expiration date in format mm/YYYY")

        if current_expiration_date <= date.today():
            raise ValueError("The Card has expired")

        return self


class RedactedCardPayload(CardPayload):
    id: Optional[str] = None
    brand: Optional[str] = None

    @model_validator(mode="after")
    def redact(self):
        self.number = f"************{self.number[12:]}"

        return self


class Card(BaseModel):
    card_holder: str = Field(
        min_length=CardConstants.HOLDER_MIN_SIZE,
        max_length=CardConstants.HOLDER_MAX_SIZE,
    )

    card_number: str = Field(
        min_length=CardConstants.CARD_NUMBER_MIN_SIZE,
        max_length=CardConstants.CARD_NUMBER_MAX_SIZE,
    )
    expiration_date: date
    cvv: str = Field(
        min_length=CardConstants.CVV_MIN_SIZE, max_length=CardConstants.CVV_MAX_SIZE
    )

    id: Optional[str] = None

    @model_validator(mode="after")
    def validate(self):
        try:
            int(self.card_number)
        except ValueError as exception:
            raise ValueError("Card number must have only numbers") from exception

        card_number = CreditCard(self.card_number)
        if not card_number.is_valid():
            raise ValueError("Card number provided is invalid")

        try:
            int(self.cvv)
        except ValueError as exception:
            raise ValueError(
                "CVV must be a number with 3 up to 4 digits"
            ) from exception

        return self

    @classmethod
    def from_payload(cls, payload: CardPayload):
        return cls(
            **{
                "expiration_date": expire_date_to_date(payload.exp_date),
                "card_holder": payload.holder,
                "card_number": payload.number,
                "cvv": payload.cvv,
            }
        )

    @classmethod
    def from_model(cls, card_model: CardModel):
        return cls(
            **{
                "id": str(card_model.id),
                "card_number": card_model.card_number,
                "card_holder": card_model.card_holder,
                "expiration_date": card_model.expiration_date,
                "cvv": card_model.cvv,
            }
        )

    def to_model(self) -> CardModel:
        transformed_data = self.model_dump()
        return CardModel(**transformed_data)

    def as_redacted_payload(self) -> RedactedCardPayload:
        """
        In order to protect sensitive information, We should output a
        redacted representation to the user
        """
        try:
            brand = CreditCard(self.card_number).get_brand()
        except BrandNotFound:
            brand = None

        return RedactedCardPayload(
            **{
                "exp_date": date_to_expire_date(self.expiration_date),
                "holder": self.card_holder,
                "number": self.card_number,
                "cvv": self.cvv,
                "brand": brand,
                "id": self.id,
            }
        )
