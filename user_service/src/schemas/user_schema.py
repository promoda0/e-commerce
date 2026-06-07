from pydantic import BaseModel, Field

from user_service.src.core.constants import UserRole


class UserSignupRequest(BaseModel):
    first_name: str = Field(..., min_length=2, max_length=32)
    last_name: str = Field(..., min_length=1, max_length=32)
    email: str = Field(..., min_length=5, max_length=120)
    phone_number: str = Field(..., min_length=7, max_length=20)
    password: str = Field(..., min_length=8, max_length=64)
    role: UserRole = UserRole.CUSTOMER


class UserLoginRequest(BaseModel):
    email: str = Field(..., min_length=5, max_length=120)
    password: str = Field(..., min_length=8, max_length=64)


class UserPublicResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    phone_number: str
    role: UserRole


class UserSignupResponse(UserPublicResponse):
    pass


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
