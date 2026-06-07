from collections.abc import Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from payment_service.app.core.constants import UserRole
from payment_service.app.core.database import SessionLocal
from payment_service.app.schemas.auth_schema import AuthenticatedUser
from payment_service.app.utils.jwt_handler import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(token: str = Depends(oauth2_scheme)) -> AuthenticatedUser:
    payload = decode_access_token(token)

    try:
        user_id = int(payload["sub"])
        role = UserRole(payload["role"])
    except (TypeError, ValueError) as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc

    return AuthenticatedUser(user_id=user_id, role=role)

