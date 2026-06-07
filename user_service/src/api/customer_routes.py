from fastapi import APIRouter, Depends

from user_service.src.auth.dependencies import get_current_user
from user_service.src.models.user import User
from user_service.src.schemas.user_schema import UserPublicResponse
from user_service.src.services.user_service import UserService

router = APIRouter(prefix="/customer", tags=["Customer"])


@router.get("/me", response_model=UserPublicResponse)
def get_customer_profile(current_user: User = Depends(get_current_user)) -> UserPublicResponse:
    return UserService.to_public_user(current_user)

