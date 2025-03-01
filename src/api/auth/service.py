from datetime import datetime, timedelta, timezone
from uuid import UUID, uuid4

import jwt

from src.api.auth.schemas import JWTData, TokenInfo, TokenType
from src.core.config import settings
from src.core.models import User


class AuthService:
    @staticmethod
    def _create_jwt(user_id: UUID, token_type: TokenType, expire_minutes: int) -> str:
        now = datetime.now(timezone.utc)
        expire = now + timedelta(minutes=expire_minutes)
        jwt_payload = JWTData(
            user_id=user_id,
            exp=expire,
            iat=now,
            jti=str(uuid4()),
            token_type=token_type,
        )
        return jwt.encode(
            jwt_payload.model_dump(mode="json"),
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

    # @staticmethod
    # def refresh_token(admin: Admin) -> TokenInfo:
    #     access_token = JWTAdminService._create_jwt(
    #         admin_id=admin.admin_id,
    #         token_type=TokenType.ACCESS,
    #         expire_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
    #     )
    #     return TokenInfo(access_token=access_token)

    # @staticmethod
    # def get_admin_info(admin: Admin, payload: JWTData) -> ValidateReturnSchema:
    #     return ValidateReturnSchema(
    #         admin_id=admin.admin_id,
    #         login=admin.login,
    #         full_name=admin.full_name,
    #         permissions=admin.permissions,
    #         token_issued_at=payload.iat,
    #         token_expires_at=payload.exp,
    #     )
