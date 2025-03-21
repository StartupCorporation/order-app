from abc import ABC, abstractmethod

from domain.service.entity.callback_request import CallbackRequest


class CallbackRequestRepository(ABC):
    @abstractmethod
    async def save(self, entity: CallbackRequest) -> None: ...
