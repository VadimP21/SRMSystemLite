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

    def get_list(
        self,
        limit: int | None,
        offset: int | None,
        sort_field: str | None,
        sort_order: str = "asc",
        **filters,
    ) -> List[Product] | None:
        try:
            query = self.session.query(ProductModel).filter_by(**filters)
            if sort_field is not None:
                column = getattr(ProductModel, sort_field, None)
                if column is not None:
                    if sort_order.lower() == "desc":
                        query = query.order_by(column.desc())
                    else:
                        query = query.order_by(column.asc())
                else:
                    print(
                        f"Warning: Sort field '{sort_field}' not found in ProductModel."
                    )
            if limit is not None:
                query = query.limit(limit)
            if offset > 0:
                query = query.offset(offset)
            products = query.all()

            return [Product(**product.dict()) for product in products]
        except SQLAlchemyError as e:
            print(f"Error getting products: {e}")
            return []

    def add(self, product: Dict[str, Any]) -> Product | None:
        try:
            record = ProductModel(**product)
            self.session.add(record)
            return Product(**record.dict(), product_=record)
        except SQLAlchemyError as e:
            print(f"Error adding product: {e}")
            return None

    def get_by_id(self, id_: int) -> Product | None:
        try:
            product = self._get_by_id(id_)
            if product:
                return Product(**product.dict())
            return None
        except SQLAlchemyError as e:
            print(f"Error getting product: {e}")
            return None

    def get_by_name(self, name_: str) -> Product | None:
        try:
            product = self._get_by_name(name_)
            if product:
                return Product(**product.dict())
            return None
        except SQLAlchemyError as e:
            print(f"Error getting product: {e}")
            return None

    def update(self, name_: str, new_product: Dict[str, Any]) -> Product | None:
        try:
            record = self._get_by_name(name_)
            if record is None:
                return None
            for key, val in new_product.items():
                setattr(record, key, val)
            return Product(**record.dict())

        except SQLAlchemyError as e:
            print(f"Error getting product: {e}")
            return None

    def delete(self, id_: int):
        try:
            record = self._get_by_id(id_)
            if record:
                self.session.delete(record)
        except SQLAlchemyError as e:
            print(f"Error deleting product: {e}")
