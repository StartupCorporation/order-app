from uuid import UUID

from dw_shared_kernel import Command


class StartOrderProcessingCommand(Command):
    order_id: UUID
