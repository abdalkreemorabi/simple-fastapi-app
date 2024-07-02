import functools
from typing import TypeVar

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

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    CELERY_BROKER_URL: str


TSettings = TypeVar("TSettings", bound=BaseSettings)


def get_settings(cls: type[TSettings]) -> TSettings:
    return cls()
