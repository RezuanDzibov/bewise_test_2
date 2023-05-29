from functools import lru_cache
from pathlib import Path

from pydantic import BaseSettings, PostgresDsn

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    PROJECT_NAME: str

    DATABASE_ENGINE: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_PORT: str
    POSTGRES_DATABASE: str
    POSTGRES_HOST: str

    API_URL: str = "http://127.0.0.1:8000"

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        return PostgresDsn.build(
            scheme=self.DATABASE_ENGINE,
            user=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_HOST,
            path=f"/{self.POSTGRES_DATABASE}",
        )

    @property
    def MEDIA_PATH(self) -> Path:
        return BASE_DIR.joinpath("media")

    class Config:
        env_file = Path(f"{BASE_DIR}/.env")


@lru_cache
def get_settings() -> Settings:
    return Settings()
