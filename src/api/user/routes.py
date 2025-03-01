from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from src.api.auth.dependencies import AccessTokenUserGetter
from src.api.user.schemas import UserCreateSchema, UserResponseSchema, UserUpdateSchema
from src.api.user.service import UserService
from src.core.models.user import User, UserRole

router = APIRouter(prefix="/user", tags=["user"])


@router.put("/", response_model=UserResponseSchema)
async def update_user(
    user_id: UUID,
    body: UserUpdateSchema,
    authorized_user: Annotated[User, Depends(AccessTokenUserGetter())],
):
    """
    Returns 404 error code if user not found or 400 error code if user with this email already exists.
    """
    if authorized_user.user_id != user_id and authorized_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not allowed to update this user")
    return await UserService.update_user(user_id, body.email, body.password_hash, body.role)


@router.get("/", response_model=UserResponseSchema)
async def get_user(
    user_id: UUID,
    authorized_user: Annotated[User, Depends(AccessTokenUserGetter())],
):
    """
    Returns 404 error code if user not found.
    """
    if authorized_user.user_id != user_id and authorized_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not allowed to get this user")
    return await UserService.get_user_by_id(user_id)


@router.post("/", response_model=UserResponseSchema)
async def create_user(body: UserCreateSchema):
    """
    Returns 400 error code if user with this email already exists.
    """
    return await UserService.create_user(body.email, body.password, body.role)
