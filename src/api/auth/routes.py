from typing import Annotated

from fastapi import APIRouter, Cookie, Depends, HTTPException, Response, status

from src.api.auth.dependencies import RefreshTokenUserGetter, validate_credentials
from src.api.auth.service import AuthService
from src.core.models import User

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/generate")
def generate_tokens(user: Annotated[User, Depends(validate_credentials)], response: Response):
    tokens = AuthService.generate_tokens(user)
    AuthService.set_auth_cookies(response, tokens)
    return {"message": "Tokens generated successfully"}


@router.post("/refresh")
def refresh_access_token(user: Annotated[User, Depends(RefreshTokenUserGetter())], response: Response):
    tokens = AuthService.refresh_tokens(user)
    AuthService.set_auth_cookies(response, tokens)
    return {"message": "Access token refreshed successfully"}


@router.get("/validate")
def is_authorized(access_token: Annotated[str | None, Cookie()], refresh_token: Annotated[str | None, Cookie()]):
    if access_token is None or refresh_token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")


@router.post("/logout")
def logout(response: Response):
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return {"message": "Logged out successfully"}
