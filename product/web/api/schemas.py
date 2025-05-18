from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import List

from pydantic import BaseModel, ConfigDict


class SortField(str, Enum):
    name = "name"
    price = "price"
    created_at = "created_at"


# Определите перечисление для направления сортировки
class SortOrder(str, Enum):
    asc = "asc"
    desc = "desc"


class CreateProductSchema(BaseModel):
    name: str
    price: Decimal


class GetProductSchema(CreateProductSchema):
    id: int
    created_at: datetime


class ProductResponse(BaseModel):
    products: List[GetProductSchema]
