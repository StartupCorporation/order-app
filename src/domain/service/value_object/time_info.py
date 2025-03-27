from dataclasses import dataclass
from datetime import datetime

from dw_shared_kernel import ValueObject


@dataclass(kw_only=True, slots=True)
class TimeInfo(ValueObject):
    created_at: datetime

    @classmethod
    def new(
        cls,
        created_at: datetime,
    ) -> "TimeInfo":
        return TimeInfo(
            created_at=created_at,
        )
