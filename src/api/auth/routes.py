from typing import Annotated

from fastapi import APIRouter, Depends, Response

from src.api.auth.dependencies import RefreshTokenUserGetter, validate_credentials
from src.api.auth.schemas import TokenInfo
from src.api.auth.service import AuthService
from src.core.config import settings
from src.core.models import User

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/generate", response_model=TokenInfo)
def generate_tokens(user: Annotated[User, Depends(validate_credentials)], response: Response):
    tokens = AuthService.generate_tokens(user)
    response.set_cookie(
        key="access_token",
        value=tokens.access_token,
        httponly=True,
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )
    response.set_cookie(
        key="refresh_token",
        value=tokens.refresh_token,
        httponly=True,
        max_age=settings.REFRESH_TOKEN_EXPIRE_MINUTES * 60,
    )
    return tokens


@router.post("/refresh", response_model=TokenInfo, response_model_exclude_none=True)
def refresh_access_token(user: Annotated[User, Depends(RefreshTokenUserGetter())]):
    return AuthService.refresh_tokens(user)
