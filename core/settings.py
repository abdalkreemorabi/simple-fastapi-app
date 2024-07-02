from typing import TypeVar, Literal

import dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

dotenv.load_dotenv()


class MongoDbSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_prefix="MONGO_DB_", case_sensitive=True, extra="ignore"
    )

    HOST: str
    PORT: int
    USERNAME: str
    PASSWORD: str
    DATABASE: str

    @property
    def uri(self):
        return f"mongodb://{self.HOST}:{self.PORT}/{self.DATABASE}"


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", case_sensitive=True, extra="ignore"
    )
    ENV: Literal["PROD", "DEV"] = "DEV"
    SECRET_KEY: str = "secret"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    CELERY_BROKER_URL: str | None = None
    SENTRY_DSN: str | None = None


TSettings = TypeVar("TSettings", bound=BaseSettings)


def get_settings(cls: type[TSettings]) -> TSettings:
    return cls()
