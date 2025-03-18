from abc import ABC, abstractmethod
from typing import Any


class DomainModelTableMapper[DOMAIN_MODEL, INPUT_DATA, COLUMNS_ENUM](ABC):
    @abstractmethod
    def to_domain_model(self, data: INPUT_DATA) -> DOMAIN_MODEL: ...

    @abstractmethod
    def from_domain_model(self, model: DOMAIN_MODEL) -> dict[COLUMNS_ENUM, Any]: ...
