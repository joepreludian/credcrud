from credcrud.card.schemas import Card as CardSchema, CardPayload
from credcrud.card.models import Card as CardModel
from credcrud.card.repositories import CardRepository
from database import db_session as default_db_session

class CardService:
    def __init__(self, db_session=default_db_session):
        self._repository = CardRepository(db_session)

    def create(self, card_payload: CardPayload):
        card_payload = CardSchema.from_payload(card_payload).to_model()
        return CardSchema.from_model(self._repository.create(card_payload))

    def get_by_id(self, id: str):
        card_model = self._repository.get_by_id(id)
        return CardSchema.from_model(card_model)

    def get_all(self):
        all_cards = self._repository.get_all()
        return [CardSchema.from_model(card) for card in all_cards]