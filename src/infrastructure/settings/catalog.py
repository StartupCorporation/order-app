from pydantic_settings import BaseSettings, SettingsConfigDict


class CatalogServiceSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="CATALOG_SERVICE_",
    )

    HOST: str
    PORT: int
    API_KEY: str
