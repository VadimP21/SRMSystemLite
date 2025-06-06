"""Бизнес логика сервиса Product"""

from product.product_service.exeptions import ProductNotFoundError


class ProductService:
    def __init__(self, product_repository):
        self.product_repository = product_repository

    def place_product(self, item):
        return self.product_repository.add(item)

    def get_product(self, product_name):
        product = self.product_repository.get_by_name(product_name)
        if product is not None:
            return product
        raise ProductNotFoundError(f"Product '{product_name}' is not found")

    def update_product(self, product_name, new_product):
        product = self.product_repository.get_by_name(product_name)
        if product is None:
            raise ProductNotFoundError(f"Product with name {product_name} is not found")
        print(product_name, new_product)
        return self.product_repository.update(product_name, new_product)

    def delete_product(self, product_id):
        product = self.product_repository.get_by_id(product_id)
        if product is None:
            raise ProductNotFoundError(f"Product with id {product_id} is not found")
        self.product_repository.delete(product_id)

    def list_products(self, **filters):
        limit = filters.pop("limit", None)
        offset = filters.pop("offset", None)
        sort_field = filters.pop("sort_field", None)
        sort_order = filters.pop("sort_order", None)

        return self.product_repository.get_list(
            limit=limit,
            offset=offset,
            sort_field=sort_field,
            sort_order=sort_order,
            **filters,
        )
