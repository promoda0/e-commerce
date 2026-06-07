from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from user_service.src.auth.jwt_handler import create_access_token
from user_service.src.core.constants import UserRole
from user_service.src.core.security import ACCESS_TOKEN_EXPIRE_DELTA, ACCESS_TOKEN_EXPIRE_MINUTES
from user_service.src.models.user import User
from user_service.src.repositories.user_repository import UserRepository
from user_service.src.schemas.user_schema import (
    TokenResponse,
    UserLoginRequest,
    UserPublicResponse,
    UserSignupRequest,
    UserSignupResponse,
)
from user_service.src.utils.helpers import hash_password, verify_password


class UserService:

    @staticmethod
    def register_user(db: Session, user_data: UserSignupRequest) -> UserSignupResponse:
        existing_user = UserRepository.get_by_email(db, user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email is already registered",
            )

        role = UserService._validate_role(user_data.role)
        hashed_password = hash_password(user_data.password)

        created_user = UserRepository.create_user(
            db,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            email=user_data.email,
            phone_number=user_data.phone_number,
            role=role.value,
            hashed_password=hashed_password,
        )

        return UserSignupResponse(**UserService._to_public_response(created_user).model_dump())

    @staticmethod
    def login_user(db: Session, login_data: UserLoginRequest) -> TokenResponse:
        user = UserRepository.get_by_email(db, login_data.email)
        if not user or not verify_password(login_data.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token = create_access_token(
            data={"sub": str(user.id), "role": user.role},
            expires_delta=ACCESS_TOKEN_EXPIRE_DELTA,
        )

        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        )

    @staticmethod
    def to_public_user(user: User) -> UserPublicResponse:
        return UserService._to_public_response(user)

    @staticmethod
    def _to_public_response(user: User) -> UserPublicResponse:
        return UserPublicResponse(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            phone_number=user.phone_number,
            role=UserRole(user.role),
        )

    @staticmethod
    def _validate_role(role: UserRole | str) -> UserRole:
        try:
            return role if isinstance(role, UserRole) else UserRole(role)
        except ValueError as exc:
            allowed_roles = ", ".join(value.value for value in UserRole)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid role. Allowed roles: {allowed_roles}",
            ) from exc
