from fastapi import FastAPI
from credcrud.card.routes import router as card_router


app = FastAPI()


@app.get("/healthcheck/", include_in_schema=False)
async def healthcheck() -> dict[str, str]:
    return {"status": "I'm alive"}


app.include_router(
    card_router, prefix="/credit-card", tags=["Credit Card"]
)
