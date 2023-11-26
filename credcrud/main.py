from fastapi import FastAPI

from credcrud.card.routes import router as card_router
from credcrud.database import db_session

app = FastAPI()
app.db_session = db_session


@app.get("/healthcheck/", include_in_schema=False)
async def healthcheck() -> dict[str, str]:
    return {"status": "I'm alive"}


app.include_router(card_router, prefix="/v1/credit-card", tags=["Credit Card"])
