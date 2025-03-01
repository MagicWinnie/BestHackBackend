from datetime import datetime, timedelta, timezone
from uuid import UUID, uuid4

import jwt
from fastapi import Response

from src.api.auth.schemas import JWTData, TokenInfo, TokenType
from src.core.config import settings
from src.core.models import User


class AuthService:
    @staticmethod
    def _create_jwt(user_id: UUID, token_type: TokenType, expire_minutes: int) -> str:
        now = datetime.now(timezone.utc)
        exp = now + timedelta(minutes=expire_minutes)
        jwt_payload = JWTData(
            user_id=str(user_id),
            exp=exp,
            iat=now,
            jti=str(uuid4()),
            token_type=token_type,
        )
        return jwt.encode(
            jwt_payload.model_dump(),
            key=settings.PRIVATE_KEY_PATH.read_text(),
            algorithm=settings.ALGORITHM,
        )

    @staticmethod
    def generate_tokens(user: User) -> TokenInfo:
        access_token = AuthService._create_jwt(
            user_id=user.user_id,
            token_type=TokenType.ACCESS,
            expire_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        )
        refresh_token = AuthService._create_jwt(
            user_id=user.user_id,
            token_type=TokenType.REFRESH,
            expire_minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES,
        )
        return TokenInfo(access_token=access_token, refresh_token=refresh_token)

    @staticmethod
    def refresh_tokens(user: User) -> TokenInfo:
        access_token = AuthService._create_jwt(
            user_id=user.user_id,
            token_type=TokenType.ACCESS,
            expire_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        )
        new_refresh_token = AuthService._create_jwt(
            user_id=user.user_id,
            token_type=TokenType.REFRESH,
            expire_minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES,
        )
        return TokenInfo(access_token=access_token, refresh_token=new_refresh_token)

    @staticmethod
    def set_auth_cookies(response: Response, tokens: TokenInfo):
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
