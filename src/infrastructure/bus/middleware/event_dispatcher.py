import json
from typing import Any, Awaitable, Callable

from dw_shared_kernel import (
    BusMiddleware,
    DomainEvent,
    IntegrationEvent,
    IntegrationEventRepository,
    MessageBrokerPublisher,
    ModelEvent,
)


class ModelEventDispatcherMiddleware(BusMiddleware):
    def __init__(
        self,
        integration_event_repository: IntegrationEventRepository,
        message_broker_publisher: MessageBrokerPublisher,
    ):
        self._integration_event_repository = integration_event_repository
        self._message_broker_publisher = message_broker_publisher

    async def __call__(
        self,
        message: ModelEvent,
        next_: Callable[[ModelEvent], Awaitable[Any]],
    ) -> Any:
        if isinstance(message, IntegrationEvent):
            event_destination = self._integration_event_repository.get_event_destination(
                event=message.__class__,
            )

            if not event_destination:
                raise ValueError(f"Unable to find a destination for the {message.__class__} integration event.")

            await self._message_broker_publisher.publish(
                message=json.dumps(message.serialize(), default=str).encode(),
                destination=event_destination,
            )

        if isinstance(message, DomainEvent):
            await next_(message)
