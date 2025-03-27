import json

from pydantic import BaseModel, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class RabbitMQSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="RABBITMQ_",
    )

    HOST: str
    PORT: int
    USERNAME: str
    PASSWORD: str

    CATALOG_RESERVATION_QUEUE: "QueueConfig"

    @field_validator("CATALOG_RESERVATION_QUEUE", mode="before")
    @classmethod
    def transform_to_queue_config(
        cls,
        value: str,
    ) -> dict:
        return json.loads(value)

    @property
    def connection_url(self) -> str:
        return f"amqp://{self.USERNAME}:{self.PASSWORD}@{self.HOST}:{self.PORT}"


class QueueConfig(BaseModel):
    NAME: str
    EXCHANGE: str
