import uuid

from sqlalchemy.exc import IntegrityError

from credcrud.card.exceptions import (
    CardAlreadyExistsException,
    CardNotFoundException,
    InvalidIDProvided,
)
from credcrud.card.models import Card as CardModel


class CardRepository:
    def __init__(self, db_session):
        self._db_session = db_session

    def create(self, card: CardModel) -> CardModel:
        with self._db_session() as db:
            card.id = uuid.uuid4()
            db.add(card)

            try:
                db.commit()
            except IntegrityError as current_exception:
                if all(
                    [
                        exc_txt in str(current_exception)
                        for exc_txt in ["card_number", "already exists"]
                    ]
                ):
                    raise CardAlreadyExistsException(
                        "A card with this number has been added"
                    )

                raise current_exception
            else:
                db.refresh(card)

            return card

    def get_by_id(self, id: str) -> CardModel:
        try:
            uuid.UUID(f"urn:uuid:{id}", version=4)
        except ValueError:
            raise InvalidIDProvided(f"The ID '{id}' is not an invalid UUID")

        with self._db_session() as db:
            found_card = db.query(CardModel).filter(CardModel.id == id).first()

            if found_card:
                return found_card

        raise CardNotFoundException(f"The Card {id} could not be found")

    def get_all(self) -> list[CardModel]:
        with self._db_session() as db:
            return db.query(CardModel).all()

    def delete(self, card: CardModel):
        with self._db_session() as db:
            db.delete(card)
            db.commit()

        return True
