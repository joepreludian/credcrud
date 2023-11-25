from fastapi import APIRouter, status
from fastapi.responses import PlainTextResponse
from pydantic import ValidationError

from credcrud.card.schemas import CardPayload, RedactedCardPayload
from credcrud.card.services import CardService

router = APIRouter()


@router.post("", response_model=RedactedCardPayload)
async def create_card(card_payload: CardPayload):
    try:
        return CardService().create(card_payload=card_payload).to_representation()

    except ValidationError as validation_exception:
        return PlainTextResponse(
            validation_exception.json(),
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            headers={"Content-Type": "application/json"},
        )
