from typing import Any

from fastapi import HTTPException, status
from jose import JWTError, jwt

from inventory_service.app.core.security import JWT_ALGORITHM, JWT_SECRET_KEY


def decode_access_token(token: str) -> dict[str, Any]:
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
    except JWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc

    if not payload.get("sub") or not payload.get("role"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return payload

