
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from user_service.src.core.dependencies import get_db
from user_service.src.schemas.user_schema import TokenResponse, UserLoginRequest, UserSignupRequest, UserSignupResponse
from user_service.src.services.user_service import UserService

router = APIRouter(tags=["Auth"])


@router.post("/signup", response_model=UserSignupResponse, status_code=status.HTTP_201_CREATED)
def signup(user: UserSignupRequest, db: Session = Depends(get_db)) -> UserSignupResponse:
    return UserService.register_user(db, user)


@router.post("/login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
def login(credentials: UserLoginRequest, db: Session = Depends(get_db)) -> TokenResponse:
    return UserService.login_user(db, credentials)
