from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_HOST: str
    DATABASE_PORT: int
    DATABASE_NAME: str

    SLACK_BOT_TOKEN: str
    SLACK_APP_TOKEN: str

    NOTION_TOKEN: str

    ENV: str

    AUTH_SECRET_KEY: str
    AUTH_ALGORITHM: str
    AUTH_MAGIC_LINK_EXPIRE_MINUTES: int
    AUTH_ACCESS_TOKEN_EXPIRE_MINUTES: int

    URL_FRONT: str
    URL_BACK: str

    QDRANT_HOST: str
    QDRANT_PORT: str
    QDRANT_API_KEY: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
        env_prefix="",
    )


SETTINGS = Settings()

ROOT_DIR = Path(__file__).parent.parent.parent
FILE_DIR = ROOT_DIR / "files"
MODELS_DIR = ROOT_DIR / "models"
