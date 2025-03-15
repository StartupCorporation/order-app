from dataclasses import dataclass
from uuid import UUID

from dw_shared_kernel import IntegrationEvent

from domain.order.value_object.order_product import OrderedProduct


@dataclass(frozen=True, slots=True, kw_only=True)
class OrderCreated(IntegrationEvent):
    __event_name__ = "OrderCreated"

    order_id: UUID
    products: list[OrderedProduct]

    def serialize(self) -> dict:
        serialized_event = super(OrderCreated, self).serialize()
        serialized_event["data"] = {
            "order_id": self.order_id,
            "products": [
                {
                    "product_id": product.product_id,
                    "quantity": product.quantity,
                }
                for product in self.products
            ],
        }
        return serialized_event

    @classmethod
    def deserialize(
        cls,
        data: dict,
    ) -> "OrderCreated":
        raise NotImplementedError("Event can't be deserialized")
