from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from user_service.src.auth.jwt_handler import decode_access_token
from user_service.src.core.constants import UserRole
from user_service.src.core.dependencies import get_db
from user_service.src.models.user import User
from user_service.src.repositories.user_repository import UserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    payload = decode_access_token(token)

    user_id_raw = payload.get("sub")
    if user_id_raw is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        user_id = int(user_id_raw)
    except (TypeError, ValueError) as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid subject in token",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc

    user = UserRepository.get_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found for token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


def get_current_admin(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != UserRole.ADMIN.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )
    return current_user


def get_current_seller(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != UserRole.SELLER.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Seller access required",
        )
    return current_user

