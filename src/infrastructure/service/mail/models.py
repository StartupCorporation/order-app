from pydantic import BaseModel


class ProductDetailsModel(BaseModel):
    name: str
    price: int
    quantity: int
