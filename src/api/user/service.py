from fastapi import HTTPException, status

from src.api.user.schemas import UserResponseSchema
from src.core.models import UserRole
from src.core.repositories import UserRepository


class UserService:
    @staticmethod
    async def get_user_by_email(email: str) -> UserResponseSchema:
        user = await UserRepository.get_user_by_email(email)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return UserResponseSchema(email=user.email, role=user.role)

    @staticmethod
    async def create_user(email: str, password_hash: str, role: UserRole) -> UserResponseSchema:
        if await UserRepository.get_user_by_email(email):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
        user = await UserRepository.create_user(email, password_hash, role)
        return UserResponseSchema(email=user.email, role=user.role)
