from uuid import UUID, uuid4

from fastapi import HTTPException, status

from src.api.user.schemas import UserResponseSchema
from src.core.auth.password_handler import PasswordHandler
from src.core.models import UserRole
from src.core.models.user import User
from src.core.repositories import UserRepository


class UserService:
    @staticmethod
    async def get_user_by_id(user_id: UUID) -> UserResponseSchema:
        user = await UserRepository.get_user_by_id(user_id)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return UserResponseSchema(user_id=user.user_id, email=user.email, role=user.role, is_active=user.is_active)

    @staticmethod
    async def update_user(
        user_id: UUID,
        email: str | None = None,
        password_hash: str | None = None,
        role: UserRole | None = None,
    ) -> UserResponseSchema:
        user = await UserRepository.get_user_by_id(user_id)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        if email is not None:
            if await UserRepository.get_user_by_email(email):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="User with this email already exists",
                )
            user.email = email
        user.password_hash = password_hash or user.password_hash
        user.role = role or user.role
        await user.save()
        return UserResponseSchema(user_id=user.user_id, email=user.email, role=user.role, is_active=user.is_active)

    @staticmethod
    async def create_user(email: str, password: str, role: UserRole) -> UserResponseSchema:
        if await UserRepository.get_user_by_email(email):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with this email already exists")
        password_hash = PasswordHandler(password).get_password_hash()
        user = User(user_id=uuid4(), email=email, password_hash=password_hash, role=role)
        await user.save()
        return UserResponseSchema(user_id=user.user_id, email=user.email, role=user.role, is_active=user.is_active)
