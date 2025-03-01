import logging
from datetime import datetime, timezone
from typing import Annotated

import jwt
from fastapi import Cookie, HTTPException, status
from pydantic import ValidationError

from src.api.auth.schemas import CredentialsSchema, JWTData, TokenType
from src.core.auth.password_handler import PasswordHandler
from src.core.config import settings
from src.core.models import User
from src.core.repositories import UserRepository
from src.core.repositories.blacklist_jwt import BlacklistJWTRepository

logger = logging.getLogger(__name__)


async def validate_credentials(creds: CredentialsSchema) -> User:
    user = await UserRepository.get_user_by_email(email=creds.email)

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not active")

    password_handler = PasswordHandler(plain_password=creds.password)
    if not password_handler.verify_password(user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")

    return user


async def get_current_token_payload(token: str) -> JWTData:
    try:
        decoded = jwt.decode(
            token,
            key=settings.PUBLIC_KEY_PATH.read_text(),
            algorithms=[settings.ALGORITHM],
            options={"verify_exp": True},
        )
        return JWTData(**decoded)
    except jwt.ExpiredSignatureError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired. Please log in again.",
        ) from e
    except (jwt.exceptions.InvalidTokenError, ValidationError) as e:
        logger.error("Invalid token error: %s", e)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token error") from e


class AccessTokenUserGetter:
    async def __call__(self, access_token: Annotated[str, Cookie()]) -> User:
        payload = await get_current_token_payload(access_token)
        if payload.token_type != TokenType.ACCESS:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid token type {payload.token_type}. Expected {TokenType.ACCESS}",
            )

        user = await UserRepository.get_user_by_id(user_id=payload.user_id)
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
        if not user.is_active:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not active")

        return user


class RefreshTokenUserGetter:
    async def __call__(self, refresh_token: Annotated[str, Cookie()]) -> User:
        payload = await get_current_token_payload(refresh_token)
        if payload.token_type != TokenType.REFRESH:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid token type {payload.token_type}. Expected {TokenType.REFRESH}",
            )

        if await BlacklistJWTRepository.is_token_blacklisted(payload.jti):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Refresh token is invalid")

        if datetime.now(timezone.utc) > payload.exp:
            await BlacklistJWTRepository.add_token_uuid_to_blacklist(payload.jti)

        user = await UserRepository.get_user_by_id(user_id=payload.user_id)
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
        if not user.is_active:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not active")

        return user
