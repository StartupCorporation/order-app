from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class RabbitMQSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="RABBITMQ_",
    )

    HOST: str
    PORT: int
    USERNAME: str
    PASSWORD: str

    @property
    def connection_url(self) -> str:
        return f"amqp://{self.USERNAME}:{self.PASSWORD}@{self.HOST}:{self.PORT}"


class QueueConfig(BaseModel):
    NAME: str
    EXCHANGE: str
