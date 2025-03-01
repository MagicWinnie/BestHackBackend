from uuid import UUID

from pydantic import BaseModel

from src.core.models import UserRole


class UserResponseSchema(BaseModel):
    user_id: UUID
    email: str
    role: UserRole
    is_active: bool
