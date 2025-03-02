import logging
from datetime import datetime, timezone
from uuid import UUID

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import ValidationError

from src.api.auth.schemas import CredentialsSchema, JWTData, TokenType
from src.core.auth.password_handler import PasswordHandler
from src.core.config import settings
from src.core.models import User
from src.core.repositories import BlacklistJWTRepository, UserRepository

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


async def get_current_token_payload(credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())) -> JWTData:
    try:
        decoded = jwt.decode(
            credentials.credentials,
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
    async def __call__(self, payload: JWTData = Depends(get_current_token_payload)) -> User:
        if payload.token_type != TokenType.ACCESS:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid token type {payload.token_type}. Expected {TokenType.ACCESS}",
            )

        user = await UserRepository.get_user_by_id(user_id=UUID(payload.user_id))
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
        if not user.is_active:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not active")

        return user


class RefreshTokenUserGetter:
    async def __call__(self, payload: JWTData = Depends(get_current_token_payload)) -> User:
        if payload.token_type != TokenType.REFRESH:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid token type {payload.token_type}. Expected {TokenType.REFRESH}",
            )

        if await BlacklistJWTRepository.is_token_blacklisted(payload.jti):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Refresh token is invalid")

        if datetime.now(timezone.utc) > payload.exp:
            await BlacklistJWTRepository.add_token_uuid_to_blacklist(payload.jti)

        user = await UserRepository.get_user_by_id(user_id=UUID(payload.user_id))
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
        if not user.is_active:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not active")

        return user
