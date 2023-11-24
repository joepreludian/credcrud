import uuid

from credcrud.card.models import Card


class CardRepository:
    def __init__(self, db_session):
        self._db_session = db_session

    def create(self, card: Card) -> Card:
        with self._db_session() as db:
            card.id = uuid.uuid4()
            db.add(card)
            db.commit()
            db.refresh(card)

            return card

    def get_by_id(self, id: str) -> Card:
        with self._db_session as db:
            return db.query(Card).filter(Card.id == id).first()