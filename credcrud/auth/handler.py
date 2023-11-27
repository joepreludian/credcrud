import os

from fastapi import HTTPException, Request, status

# Hardcoded token for demonstration purposes
SECRET_TOKEN = os.environ.get("API_TOKEN", "your_secret_token")  # nosec


def require_simple_token(request: Request):
    authorization: str = request.headers.get("Authorization")
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
        )

    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or token != SECRET_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
        )

    return token
