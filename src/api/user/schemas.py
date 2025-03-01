from uuid import UUID

from pydantic import BaseModel

from src.core.models import UserRole


class UserResponseSchema(BaseModel):
    user_id: UUID
    email: str
    role: UserRole
    is_active: bool


class UserUpdateSchema(BaseModel):
    email: str | None = None
    password_hash: str | None = None
    role: UserRole | None = None
    is_active: bool | None = None
