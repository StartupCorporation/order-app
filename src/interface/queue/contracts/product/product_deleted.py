from typing import Literal

from pydantic import BaseModel, UUID4

from application.commands.delete_product_comments.command import DeleteProductCommentsCommand
from interface.queue.contracts.base import MessageBrokerEvent


type ProductDeletedEventInputContract = MessageBrokerEvent[Literal["PRODUCTS_DELETED"], DeletedProductsData]


class DeletedProductsData(BaseModel):
    ids: list[UUID4]

    def to_command(self) -> DeleteProductCommentsCommand:
        return DeleteProductCommentsCommand(
            product_ids=self.ids,
        )
