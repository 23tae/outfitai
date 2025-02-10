from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    OPENAI_API_KEY: str
    MODEL: str = "gpt-4o-mini"
    TEMP_DIRECTORY: str = "tmp"
    IMG_THRESHOLD: int = 512
    LOG_LEVEL: str = "INFO"
    BATCH_SIZE: int = 10

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()
