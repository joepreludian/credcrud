from sqlalchemy import Column, String, Integer, Date
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from credcrud.database import Base

from credcrud.card.constants import CardConstants

class Card(Base):
    __tablename__ = "cards"

    id = Column(UUID(as_uuid=True), unique=True, primary_key=True, index=True)
    card_number = Column(String(CardConstants.CARD_NUMBER_SIZE.value), unique=True, nullable=False)
    card_holder = Column(String(CardConstants.HOLDER_MAX_SIZE.value), nullable=False)
    expiration_date = Column(Date, nullable=False)
    cvv = Column(String(CardConstants.CVV_MAX_SIZE.value), nullable=True)
