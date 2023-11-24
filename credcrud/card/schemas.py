from pydantic import BaseModel, Field, ValidationError, field_validator
from credcrud.card.constants import CardConstants
from datetime import datetime, timedelta


class Card(BaseModel):
    card_holder: str = Field(min_length=CardConstants.HOLDER_MIN_SIZE,
                             max_length=CardConstants.HOLDER_MAX_SIZE)

    card_number: str
    expiration_date: str
    cvv: str = Field(min_length=CardConstants.CVV_MIN_SIZE,
                max_length=CardConstants.CVV_MAX_SIZE)

