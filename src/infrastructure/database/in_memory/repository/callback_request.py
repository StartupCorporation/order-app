from domain.service.entity.callback_request import CallbackRequest
from domain.service.repository.callback_request import CallbackRequestRepository


class InMemoryCallbackRequestRepository(CallbackRequestRepository):
    def __init__(self) -> None:
        self._storage: set[CallbackRequest] = set()

    async def save(
        self,
        entity: CallbackRequest,
    ) -> None:
        self._storage.add(entity)

    async def get_all(self) -> list[CallbackRequest]:
        return list(self._storage)
