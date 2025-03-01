from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "BestHack API"
    PROJECT_VERSION: str = "0.1.0"
    PROJECT_DESCRIPTION: str = "API for BestHack"

    MONGODB_HOST: str = Field(default=...)
    MONGO_INITDB_ROOT_USERNAME: str = Field(default=...)
    MONGO_INITDB_ROOT_PASSWORD: str = Field(default=...)

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
