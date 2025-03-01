from uuid import UUID

from fastapi import APIRouter, Depends

from src.api.user.schemas import UserResponseSchema
from src.api.user.service import UserService
from src.core.auth.api_key import APIKeyAuth
from src.core.config import settings
from src.core.models import UserRole

router = APIRouter(prefix="/user", tags=["user"])


@router.post("/", response_model=UserResponseSchema, dependencies=[Depends(APIKeyAuth(settings.APP_API_KEY))])
async def create_user(email: str, password_hash: str, role: UserRole):
    """
    Returns 400 error code if user already exists.
    """
    return await UserService.create_user(email, password_hash, role)


@router.put("/", response_model=UserResponseSchema, dependencies=[Depends(APIKeyAuth(settings.APP_API_KEY))])
async def update_user(
    user_id: UUID,
    email: str | None = None,
    password_hash: str | None = None,
    role: UserRole | None = None,
):
    """
    Returns 404 error code if user not found.
    """
    return await UserService.update_user(user_id, email, password_hash, role)


@router.get("/", response_model=UserResponseSchema)
async def get_user(user_id: UUID):
    """
    Returns 404 error code if user not found.
    """
    return await UserService.get_user_by_id(user_id)
