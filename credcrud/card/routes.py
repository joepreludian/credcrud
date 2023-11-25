from fastapi import APIRouter, status
from fastapi.responses import JSONResponse, PlainTextResponse
from pydantic import ValidationError

from credcrud.card.exceptions import CardAlreadyExistsException
from credcrud.card.schemas import CardPayload, RedactedCardPayload
from credcrud.card.services import CardService

router = APIRouter()


@router.post("", response_model=RedactedCardPayload)
async def create_card(card_payload: CardPayload):
    try:
        return CardService().create(card_payload=card_payload).as_redacted_payload()

    except ValidationError as validation_exception:
        return PlainTextResponse(
            validation_exception.json(),
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            headers={"Content-Type": "application/json"},
        )

    except CardAlreadyExistsException as exc:
        return JSONResponse(
            {"error": str(exc)}, status_code=status.HTTP_400_BAD_REQUEST
        )
