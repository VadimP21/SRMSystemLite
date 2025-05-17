from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class CreateProductSchema(BaseModel):
    name: str
    price: Decimal


class GetProductSchema(CreateProductSchema):
    id: int
    created_at: datetime
