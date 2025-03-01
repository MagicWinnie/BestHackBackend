from uuid import UUID

from fastapi import APIRouter, Depends

from src.api.auth.dependencies import AccessTokenUserGetter
from src.api.user.schemas import UserResponseSchema, UserUpdateSchema
from src.api.user.service import UserService

router = APIRouter(prefix="/user", tags=["user"])


@router.put("/", response_model=UserResponseSchema, dependencies=[Depends(AccessTokenUserGetter())])
async def update_user(user_id: UUID, body: UserUpdateSchema):
    """
    Returns 404 error code if user not found or 400 error code if user with this email already exists.
    """
    return await UserService.update_user(user_id, body.email, body.password_hash, body.role)


@router.get("/", response_model=UserResponseSchema, dependencies=[Depends(AccessTokenUserGetter())])
async def get_user(user_id: UUID):
    """
    Returns 404 error code if user not found.
    """
    return await UserService.get_user_by_id(user_id)
