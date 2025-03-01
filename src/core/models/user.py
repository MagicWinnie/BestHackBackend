from enum import Enum

from beanie import Document


class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"


class User(Document):
    email: str
    password_hash: str
    role: UserRole
