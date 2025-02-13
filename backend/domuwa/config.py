from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SESSION_MIDDLEWARE_KEY: str = Field(default="gucci", frozen=True)
    API_PORT: int = Field(default=8000, frozen=True)
    DATABASE_URL: str = Field(default="sqlite:///db.sqlite3", frozen=True)
    # noinspection PyDataclass
    ALLOWED_ORIGINS: list[str] = Field(default=["*"], frozen=True)
    SECRET_KEY: str = Field(default="secret", frozen=True)
    HASH_ALGORITHM: str = Field(default="HS256", frozen=True)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=15, frozen=True)
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(default=7, frozen=True)

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


settings = Settings()
