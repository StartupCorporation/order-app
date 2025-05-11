from pydantic_settings import BaseSettings, SettingsConfigDict


class IACSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="IAC_",
    )

    HOST: str
    PORT: int
    API_KEY: str
