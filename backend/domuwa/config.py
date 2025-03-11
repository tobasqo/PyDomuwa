from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SESSION_MIDDLEWARE_KEY: str = "gucci"
    API_PORT: int = 8000
    DATABASE_URL: str = "sqlite:///db.sqlite3"
    # noinspection PyDataclass
    ALLOWED_ORIGINS: list[str] = ["http://localhost:5173"]
    SECRET_KEY: str = "secret"
    HASH_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        frozen=True,
    )


settings = Settings()
