from datetime import datetime

from domain.service.value_object.time_info import TimeInfo


def test_time_info_can_be_created() -> None:
    TimeInfo.new(
        created_at=datetime.now(),
    )
