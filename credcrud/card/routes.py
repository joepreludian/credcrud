from fastapi import APIRouter


router = APIRouter()


@router.get("/{uuid}")
async def create_card(uuid: str):
    return {"response": "create card: " + uuid}
