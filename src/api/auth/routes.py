from typing import Annotated

from fastapi import APIRouter, Depends, Response

from src.api.auth.dependencies import RefreshTokenUserGetter, get_current_token_payload, validate_credentials
from src.api.auth.schemas import JWTData, TokenInfo
from src.api.auth.service import AuthService
from src.core.models import User

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/generate", response_model=TokenInfo)
def generate_tokens(user: Annotated[User, Depends(validate_credentials)], response: Response):
    return AuthService.generate_tokens(user)


@router.post("/validate", response_model=JWTData)
def validate_token(payload: Annotated[JWTData, Depends(get_current_token_payload)]):
    return payload


@router.post("/refresh", response_model=TokenInfo)
def refresh_access_token(user: Annotated[User, Depends(RefreshTokenUserGetter())], response: Response):
    return AuthService.refresh_tokens(user)
