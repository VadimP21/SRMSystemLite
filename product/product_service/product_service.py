"""Бизнес логика сервиса Product"""
from product.product_service.exeptions import ProductNotFoundError


class ProductService:
    def __init__(self, product_repository):
        self.product_repository = product_repository

    def place_product(self, items):
        self.product_repository.add(items)

    def get_product(self, product_name):
        product = self.product_repository.get(product_name)
        if product is not None:
            return product
        raise ProductNotFoundError(f"Product with id {product_name} is not found")

    def update_product(self, product_name, new_product):
        product = self.product_repository.get(product_name)
        if product is None:
            raise ProductNotFoundError(f"Product with id {product_name} is not found")
        self.product_repository.update(product_name, new_product)

    def delete_product(self, product_name):
        product = self.product_repository.get(product_name)
        if product is None:
            raise ProductNotFoundError(f"Product with id {product_name} is not found")
        self.product_repository.delete(product_name)

    def list_products(self, **filters):
        limit = filters.pop("limit", None)
        self.product_repository.get_list(limit, **filters)