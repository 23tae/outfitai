from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    OPENAI_API_KEY: str
    OPENAI_MODEL: str = "gpt-4o-mini"
    OPENAI_MAX_TOKENS: int = 300
    BATCH_SIZE: int = 10
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.OPENAI_API_KEY is None:
            raise ValueError(
                "OPENAI_API_KEY must be provided either through environment variables, "
                ".env file, or directly to the constructor")

    @classmethod
    def from_dict(cls, settings_dict: dict) -> 'Settings':
        """Create Settings instance from dictionary."""
        return cls(**settings_dict)
