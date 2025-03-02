from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent.parent  # repo root folder


class Settings(BaseSettings):
    PROJECT_NAME: str = "BestHack API"
    PROJECT_VERSION: str = "0.1.0"
    PROJECT_DESCRIPTION: str = "API for BestHack"

    MONGODB_HOST: str = Field(default=...)
    MONGO_INITDB_ROOT_USERNAME: str = Field(default=...)
    MONGO_INITDB_ROOT_PASSWORD: str = Field(default=...)

    PRIVATE_KEY_PATH: Path = BASE_DIR / "certs" / "jwt-private.pem"
    PUBLIC_KEY_PATH: Path = BASE_DIR / "certs" / "jwt-public.pem"
    ALGORITHM: str = "RS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 1  # 1 day in minutes
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 30  # 30 days in minutes

    FTP_TIMEOUT: int = 3  # in seconds

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
