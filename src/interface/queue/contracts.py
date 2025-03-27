from datetime import datetime

from pydantic import UUID4, BaseModel


class MessageBrokerEvent[EVENT_TYPE, EVENT_DATA](BaseModel):
    id: UUID4
    created_at: datetime
    event_type: EVENT_TYPE
    data: EVENT_DATA
