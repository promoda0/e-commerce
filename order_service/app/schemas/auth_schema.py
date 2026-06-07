from pydantic import BaseModel

from order_service.app.core.constants import UserRole


class AuthenticatedUser(BaseModel):
    user_id: int
    role: UserRole

