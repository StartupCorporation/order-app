from typing import Any, Awaitable, Callable

from dw_shared_kernel import BusMiddleware

from infrastructure.database.base.transaction import DatabaseTransactionManager


class TransactionMiddleware(BusMiddleware):
    def __init__(
        self,
        transaction_manager: DatabaseTransactionManager,
    ):
        self._transaction_manager = transaction_manager

    async def __call__(
        self,
        message: Any,
        next_: Callable[[Any], Awaitable[Any]],
    ) -> Any:
        async with self._transaction_manager.begin():
            return await next_(message)
