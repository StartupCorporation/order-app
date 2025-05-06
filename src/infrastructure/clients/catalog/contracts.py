from uuid import UUID

from pydantic import BaseModel


class GetProductDetailsContract(BaseModel):
    name: str
    id: UUID
    price: int
