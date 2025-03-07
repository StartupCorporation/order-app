from uuid import UUID

from dw_shared_kernel import Command


class MarkOrderAsFailedForProductsReservationCommand(Command):
    order_id: UUID
