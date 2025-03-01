from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel


class TokenType(str, Enum):
    ACCESS = "access"
    REFRESH = "refresh"


class JWTData(BaseModel):
    user_id: UUID
    exp: datetime
    iat: datetime
    jti: str
    token_type: TokenType


class TokenInfo(BaseModel):
    access_token: str
    refresh_token: str


class CredentialsSchema(BaseModel):
    email: str
    password: str
