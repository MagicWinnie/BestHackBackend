from uuid import UUID, uuid4

from src.core.models import User, UserRole


class UserRepository:
    @staticmethod
    async def get_user_by_id(user_id: UUID) -> User | None:
        return await User.find_one({"user_id": user_id})

    @staticmethod
    async def get_user_by_email(email: str) -> User | None:
        return await User.find_one({"email": email})

    @staticmethod
    async def create_user(email: str, password_hash: str, role: UserRole) -> User:
        return await User(user_id=uuid4(), email=email, password_hash=password_hash, role=role).insert()
