from collections.abc import Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from product_service.app.core.constants import UserRole
from product_service.app.core.database import SessionLocal
from product_service.app.schemas.auth_schema import AuthenticatedUser
from product_service.app.utils.jwt_handler import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(token: str = Depends(oauth2_scheme)) -> AuthenticatedUser:
    payload = decode_access_token(token)

    user_id_raw = payload.get("sub")
    role_raw = payload.get("role")

    try:
        user_id = int(user_id_raw)
        role = UserRole(role_raw)
    except (TypeError, ValueError) as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc

    return AuthenticatedUser(user_id=user_id, role=role)


def get_current_seller_or_admin(
    current_user: AuthenticatedUser = Depends(get_current_user),
) -> AuthenticatedUser:
    if current_user.role not in {UserRole.SELLER, UserRole.ADMIN}:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only sellers and admins can perform this action",
        )
    return current_user

