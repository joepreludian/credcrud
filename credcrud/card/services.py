from credcrud.card.schemas import Card as CardSchema
from credcrud.card.models import Card
from credcrud.database import use_db

class CardService:
    def __init__(self, card: CardSchema = None):
        self._card = card

    def persist_to_database(self) -> str:
        pass

    def get_from_database(self, uuid: str) -> CardSchema:
        pass