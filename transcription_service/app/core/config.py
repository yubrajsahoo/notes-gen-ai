from importlib.metadata import metadata, version

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings class that inherits from BaseSettings.
    """

    # environment variables
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"
    API_PREFIX: str = "/api/v1"

    # Extract static build-time metadata from pyproject.toml
    @property
    def PROJECT_NAME(self) -> str:
        return metadata("transcription_service")["Name"]

    @property
    def VERSION(self) -> str:
        return version("transcription_service")

    # Load overrides from a local .env file securely
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=True, extra="ignore"
    )


# Create an instance of the settings class
settings = Settings()
