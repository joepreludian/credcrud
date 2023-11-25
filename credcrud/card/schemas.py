from pydantic import BaseModel, Field, ValidationError, field_validator, model_validator
from credcrud.card.constants import CardConstants
from credcrud.card.models import Card as CardModel
from credcrud.card.utils import standardize_expire_date, format_standard_date_to_expire_date
from datetime import datetime, timedelta
from typing import Optional
from creditcard import CreditCard
from creditcard.exceptions import BrandNotFound

class CardPayload(BaseModel):
    exp_date: str
    holder: str
    number: str
    cvv: str

    id: Optional[str] = None
    brand: Optional[str] = None

class Card(BaseModel):
    card_holder: str = Field(min_length=CardConstants.HOLDER_MIN_SIZE,
                             max_length=CardConstants.HOLDER_MAX_SIZE)

    card_number: str = Field(min_length=CardConstants.CARD_NUMBER_MIN_SIZE,
                             max_length=CardConstants.CARD_NUMBER_MAX_SIZE)
    expiration_date: str
    cvv: str = Field(min_length=CardConstants.CVV_MIN_SIZE,
                max_length=CardConstants.CVV_MAX_SIZE)


    @model_validator(mode='after')
    def validate(self):

        try:
            int(self.card_number)
        except ValueError as exception:
            raise ValueError("Card number must have only numbers") from exception

        card_number = CreditCard(self.card_number)
        if not card_number.is_valid():
            raise ValueError("Card number provided is invalid")

        try:
            self.expiration_date = standardize_expire_date(self.expiration_date)
        except ValueError as exception:
            raise ValueError("Card exp_date must be on mm/YYYY format") from exception

        try:
            int(self.cvv)
        except ValueError as exception:
            raise ValueError("CVV must be a number with 3 up to 4 digits") from exception

        return self


    @classmethod
    def from_payload(cls, payload: CardPayload):
        return cls(**{
            "expiration_date": payload.exp_date,
            "card_holder": payload.holder,
            "card_number": payload.number,
            "cvv": payload.cvv,
        })

    def to_model(self) -> CardModel:
        transformed_data = self.dict()

        transformed_data['expiration_date'] = (
            datetime.strptime(transformed_data['expiration_date'], '%Y-%m-%d').date())

        return CardModel(**transformed_data)

    def to_representation(self) -> CardPayload:
        """
        In order to protect sensitive information, We should output a redacted representation to the user
        """
        try:
            brand = CreditCard(self.card_number).get_brand()
        except BrandNotFound:
            brand = None

        return CardPayload(**{
            "exp_date": format_standard_date_to_expire_date(self.expiration_date),
            "holder": self.card_holder,
            "number": f"************{self.card_number[12:]}",
            "cvv": self.cvv,
            "brand": brand
        })