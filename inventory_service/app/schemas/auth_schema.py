from pydantic import BaseModel

from inventory_service.app.core.constants import UserRole


class AuthenticatedUser(BaseModel):
    user_id: int
    role: UserRole

