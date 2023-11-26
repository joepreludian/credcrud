from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse, PlainTextResponse
from pydantic import ValidationError
from credcrud.auth.handler import require_simple_token

from credcrud.card.exceptions import CardAlreadyExistsException, CardNotFoundException
from credcrud.card.schemas import CardPayload, RedactedCardPayload
from credcrud.card.services import CardService

router = APIRouter(dependencies=[
    Depends(require_simple_token)
])


@router.post("", response_model=RedactedCardPayload, status_code=status.HTTP_201_CREATED)
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


@router.get("/{id}", response_model=RedactedCardPayload)
async def get_card(id: str):
    try:
        return CardService().get_by_id(id).as_redacted_payload()

    except ValidationError as validation_exception:
        return PlainTextResponse(
            validation_exception.json(),
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            headers={"Content-Type": "application/json"},
        )

    except CardNotFoundException as exc:
        return JSONResponse({"error": str(exc)}, status_code=status.HTTP_404_NOT_FOUND)


@router.get("", response_model=list[RedactedCardPayload])
async def get_all_cards():
    return (card.as_redacted_payload() for card in CardService().get_all())


@router.delete("/{id}", response_model=None, status_code=status.HTTP_204_NO_CONTENT)
async def delete_card(id:str):
    try:
        CardService().delete(id)
    except CardNotFoundException as exc:
        return JSONResponse({"error": str(exc)}, status_code=status.HTTP_404_NOT_FOUND)
