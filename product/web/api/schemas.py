from datetime import datetime
from decimal import Decimal
from typing import List

from pydantic import BaseModel, ConfigDict


class CreateProductSchema(BaseModel):
    name: str
    price: Decimal


class GetProductSchema(CreateProductSchema):
    id: int
    created_at: datetime

class ProductResponse(BaseModel):
    products: List[GetProductSchema]
