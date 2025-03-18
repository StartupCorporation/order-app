from dataclasses import dataclass
from uuid import UUID

from dw_shared_kernel import IntegrationEvent


@dataclass(frozen=True, slots=True, kw_only=True)
class OrderSubmittedForProcessing(IntegrationEvent):
    __event_name__ = "OrderSubmittedForProcessing"

    order_id: UUID

    def serialize(self) -> dict:
        serialized_event = super(OrderSubmittedForProcessing, self).serialize()
        serialized_event["data"] = {
            "order_id": self.order_id,
        }
        return serialized_event

    @classmethod
    def deserialize(
        cls,
        data: dict,
    ) -> "OrderSubmittedForProcessing":
        raise NotImplementedError("Event can't be deserialized")
