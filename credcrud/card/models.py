from sqlalchemy import Column, Date, String, Text
from sqlalchemy.dialects.postgresql import UUID

from credcrud.card.constants import CardConstants
from credcrud.database import Base


class Card(Base):
    __tablename__ = "cards"

    id = Column(UUID(as_uuid=True), unique=True, primary_key=True, index=True)
    card_number = Column(Text(), unique=True, nullable=False)
    card_holder = Column(String(CardConstants.HOLDER_MAX_SIZE.value), nullable=False)
    expiration_date = Column(Date, nullable=False)
    cvv = Column(String(CardConstants.CVV_MAX_SIZE.value), nullable=True)
