from pydantic import UUID4, BaseModel


class GetProductDetailsContract(BaseModel):
    name: str
    id: UUID4
    price: int
