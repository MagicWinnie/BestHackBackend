from typing import Annotated

from fastapi import APIRouter, Depends, Response

from src.api.auth.dependencies import RefreshTokenUserGetter, validate_credentials
from src.api.auth.schemas import TokenInfo
from src.api.auth.service import AuthService
from src.core.models import User

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/generate", response_model=TokenInfo)
def generate_tokens(user: Annotated[User, Depends(validate_credentials)], response: Response):
    return AuthService.generate_tokens(user)


@router.post("/refresh", response_model=TokenInfo)
def refresh_access_token(user: Annotated[User, Depends(RefreshTokenUserGetter())], response: Response):
    return AuthService.refresh_tokens(user)
