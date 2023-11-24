import uuid

from credcrud.card.schemas import Card as CardSchema
from credcrud.card.models import Card
from credcrud.database import database_session

from datetime import datetime


class TestCardService:

    def test_fetch_card(self, db_session):
        db_card = Card(
            id=uuid.uuid4(),
            card_number="0000111122223333",
            card_holder="Jonhnatha Trigueiro",
            expiration_date=datetime.now(),
            cvv="1234"
        )

        db_session.add(db_card)
        db_session.commit()
        db_session.refresh(db_card)