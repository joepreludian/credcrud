from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse, PlainTextResponse
from pydantic import ValidationError

from credcrud.auth.handler import require_simple_token
from credcrud.card.exceptions import CardNotFoundException, InvalidIDProvided
from credcrud.card.schemas import CardPayload, RedactedCardPayload
from credcrud.card.services import CardService
from credcrud.database import db_session

router = APIRouter(dependencies=[Depends(require_simple_token)])

router.db_session = db_session


@router.post(
    "", response_model=RedactedCardPayload, status_code=status.HTTP_201_CREATED
)
async def create_card(card_payload: CardPayload):
    try:
        return (
            CardService(router.db_session)
            .create(card_payload=card_payload)
            .as_redacted_payload()
        )

    except ValidationError as validation_exception:
        return PlainTextResponse(
            validation_exception.json(),
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            headers={"Content-Type": "application/json"},
        )


@router.get("/{id}", response_model=RedactedCardPayload)
async def get_card(id: str):
    try:
        return CardService(router.db_session).get_by_id(id).as_redacted_payload()

    except CardNotFoundException as exc:
        return JSONResponse({"error": str(exc)}, status_code=status.HTTP_404_NOT_FOUND)

    except InvalidIDProvided as exc:
        return JSONResponse(
            {"error": str(exc)}, status_code=status.HTTP_400_BAD_REQUEST
        )


@router.get("", response_model=list[RedactedCardPayload])
async def get_all_cards():
    return (
        card.as_redacted_payload() for card in CardService(router.db_session).get_all()
    )


@router.delete("/{id}", response_model=None, status_code=status.HTTP_204_NO_CONTENT)
async def delete_card(id: str):
    try:
        CardService(router.db_session).delete(id)
    except CardNotFoundException as exc:
        return JSONResponse({"error": str(exc)}, status_code=status.HTTP_404_NOT_FOUND)
    except InvalidIDProvided as exc:
        return JSONResponse(
            {"error": str(exc)}, status_code=status.HTTP_400_BAD_REQUEST
        )
