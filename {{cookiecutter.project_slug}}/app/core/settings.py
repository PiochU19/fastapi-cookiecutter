from enum import Enum
from typing import Any, Dict, List

from core.exceptions import AppConfigurationException
from pydantic import BaseSettings, Field, root_validator, validator


class Environments(str, Enum):
    PRODUCTION: str = "PRODUCTION"
    DEVELOPMENT: str = "DEVELOPMENT"


class Settings(BaseSettings):
    ENV: str = Field(..., env="ENVIRONMENT")
    DB_USER: str = Field(..., env="POSTGRES_USER")
    DB_PASSWORD: str = Field(..., env="POSTGRES_PASSWORD")
    DB_NAME: str = Field(..., env="POSTGRES_DB")
    ALLOWED_ORIGINS: List[str] = Field(..., env="ALLOWED_ORIGINS")
    DB_HOST: str = Field(..., env="SQL_HOST")
    DB_PORT: int = Field(..., env="SQL_PORT")

    @property
    def database_url(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @root_validator
    def validate_allowed_origins(cls, values: Dict[str, Any]) -> None:
        if (
            values["ENV"] == Environments.PRODUCTION
            and "*" in values["ALLOWED_ORIGINS"]
        ):
            raise AppConfigurationException(
                f"You cannot trust all hosts in {Environments.PRODUCTION} environment."
            )

        return values

    @validator("ENV")
    def validate_env(cls, env: str) -> str:
        if env not in Environments.__members__:
            raise AppConfigurationException(f"Unknown environment: {env}.")

        return env

    class Config:
        use_enum_values = True


settings = Settings()
CURRENT_ENV = settings.ENV
