from pydantic_settings import BaseSettings, SettingsConfigDict


class SMTPSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="SMTP_",
    )

    HOST: str
    PORT: int
    TIMEOUT: int
    USE_TLS: bool

    SENDER_EMAIL: str

    USERNAME: str | None = None
    PASSWORD: str | None = None
