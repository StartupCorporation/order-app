from pydantic_settings import BaseSettings, SettingsConfigDict


class ApplicationSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="APPLICATION_",
    )

    TITLE: str
    DEBUG: bool
    VERSION: str
