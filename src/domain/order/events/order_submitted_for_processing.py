from dataclasses import dataclass

from dw_shared_kernel import IntegrationEvent

from domain.order.value_object.ordered_product import OrderedProduct


@dataclass(frozen=True, slots=True, kw_only=True)
class OrderSubmittedForProcessing(IntegrationEvent):
    __event_name__ = "ORDER_SUBMITTED_FOR_PROCESSING"

    products: list[OrderedProduct]

    def serialize(self) -> dict:
        serialized_event = super(OrderSubmittedForProcessing, self).serialize()
        serialized_event["data"] = [
            {
                "product_id": product.product_id,
                "quantity": product.quantity,
            }
            for product in self.products
        ]
        return serialized_event

    @classmethod
    def deserialize(
        cls,
        data: dict,
    ) -> "OrderSubmittedForProcessing":
        raise NotImplementedError("Event can't be deserialized")
