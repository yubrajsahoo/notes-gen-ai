from typing import Any

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "Transcription API"
    HOST: str = "localhost"
    PORT: int = 8000
    RELOAD: bool = True
    DEBUG: bool = True
    CORS_ORIGINS: list[str] = ["*"]

    # This tells Pydantic to automatically look for a .env file
    # to override the defaults above
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    def __getattr__(self, item: str) -> Any:
        upper_item = item.upper()
        if upper_item in type(self).model_fields:
            return getattr(self, upper_item)
        return super().__getattr__(item)


settings = Settings()
