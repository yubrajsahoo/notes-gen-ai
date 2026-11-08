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

    @property
    def cors_origins(self) -> list[str]:
        return self.CORS_ORIGINS


settings = Settings()
