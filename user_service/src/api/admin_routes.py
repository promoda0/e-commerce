from fastapi import APIRouter, Depends

from user_service.src.auth.dependencies import get_current_admin
from user_service.src.models.user import User
from user_service.src.schemas.user_schema import UserPublicResponse
from user_service.src.services.user_service import UserService

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/me", response_model=UserPublicResponse)
def get_admin_profile(current_user: User = Depends(get_current_admin)) -> UserPublicResponse:
    return UserService.to_public_user(current_user)

