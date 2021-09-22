import os

from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Pitch APP"
    DESCRIPTION:str = "FastAPI POC"
    VERSION: int = 2.0
    SQLALCHEMY_DATABASE_URL: str = 'postgresql+psycopg2://nytro_pitch:nytro@127.0.0.1:5432/fastapi'
    APP_ROOT_DIR: str = os.path.dirname(os.path.dirname(__file__))
    STATIC_PATH: str = os.path.abspath(os.path.join(APP_ROOT_DIR, "static"))


@lru_cache()
def _settings():
    return Settings()


settings = _settings()
