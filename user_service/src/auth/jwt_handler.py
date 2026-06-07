import importlib
from datetime import datetime, timedelta, timezone
from typing import Any

from fastapi import HTTPException, status

from user_service.src.core.security import JWT_ALGORITHM, JWT_SECRET_KEY

jose_jwt = importlib.import_module("jose.jwt")
JWTError = importlib.import_module("jose.exceptions").JWTError


def create_access_token(data: dict[str, Any], expires_delta: timedelta) -> str:
    to_encode: dict[str, Any] = dict(data)
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode["exp"] = expire
    return jose_jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)


def decode_access_token(token: str) -> dict[str, Any]:
    try:
        payload = jose_jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
    except JWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc

    subject = payload.get("sub")
    if not subject:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return payload
