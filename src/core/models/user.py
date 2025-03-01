from enum import Enum
from uuid import UUID

from beanie import Document


class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"


class User(Document):
    user_id: UUID
    email: str
    password_hash: str
    role: UserRole
    is_active: bool = True
