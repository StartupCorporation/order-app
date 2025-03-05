from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="DATABASE_",
    )

    HOST: str
    PORT: int
    DATABASE: str
    USERNAME: str
    PASSWORD: str

    def get_database_url(
        self,
        driver: str,
    ) -> str:
        return f"{driver}://{self.USERNAME}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DATABASE}"
