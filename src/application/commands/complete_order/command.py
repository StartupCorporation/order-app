from dw_shared_kernel import Command
from pydantic import UUID4


class CompleteOrderCommand(Command):
    order_id: UUID4
