from typing import Dict, Any, List

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from product.product_repository.models import ProductModel
from product.product_service.products import Product


class ProductRepository:
    """
    Репозиторий для Product
    Основные функции:
                    принимают Dict[str, Any], int,
                    возвращают Product | List[Product] |None
    Внутренние функции:
                    возвращают модели БД

    """

    def __init__(self, session: Session):
        self.session = session

    def _get_by_id(self, id_: int) -> ProductModel | None:
        try:
            return (
                self.session.query(ProductModel).filter(ProductModel.id == id_).first()
            )
        except SQLAlchemyError as e:
            print(f"Error getting product: {e}")
            return None

    def _get_by_name(self, name_: str) -> ProductModel | None:
        try:
            return (
                self.session.query(ProductModel)
                .filter(ProductModel.name == name_)
                .first()
            )
        except SQLAlchemyError as e:
            print(f"Error getting product: {e}")
            return None

    def add(self, product: Dict[str, Any]) -> Product | None:
        try:
            record = ProductModel(**product)
            self.session.add(record)
            return Product(**record.dict(), product_=record)
        except SQLAlchemyError as e:
            print(f"Error adding product: {e}")
            return None

    def get_one_by_name(self, name_: str) -> Product | None:
        try:
            product = self._get_by_name(name_)
            if product:
                return Product(**product.dict())
            return None
        except SQLAlchemyError as e:
            print(f"Error getting product: {e}")
            return None

    def get_list(self, limit, **filters) -> List[Product] | None:
        try:
            query = self.session.query(ProductModel)
            products = query.filter_by(**filters).limit(limit).all()
            return [Product(**product.dict()) for product in products]
        except SQLAlchemyError as e:
            print(f"Error getting products: {e}")
            return None
