from pydantic import BaseModel

from src.core.models import UserRole


class UserResponseSchema(BaseModel):
    email: str
    role: UserRole
