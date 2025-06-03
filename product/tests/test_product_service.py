import unittest
from unittest.mock import MagicMock

from product.product_service.exeptions import ProductNotFoundError
from product.product_service.product_service import ProductService


class TestProductService(unittest.TestCase):

    def setUp(self):
        """Настройка перед каждым тестом."""
        self.mock_repository = MagicMock()
        self.product_service = ProductService(self.mock_repository)

    def test_init(self):
        """Тест инициализации сервиса."""
        self.assertEqual(self.product_service.product_repository, self.mock_repository)

    def test_place_product_calls_repository_add(self):
        """Тест place_product вызывает метод add репозитория."""
        test_item = {"name": "New Product", "price": 100}
        self.mock_repository.add.return_value = {"id": 1, **test_item}

        result = self.product_service.place_product(test_item)

        self.mock_repository.add.assert_called_once_with(test_item)
        self.assertEqual(result, {"id": 1, **test_item})

    def test_get_product_found(self):
        """Тест get_product возвращает продукт, если найден."""
        product_name = "Existing Product"
        mock_product = {"id": 1, "name": product_name, "price": 50}
        self.mock_repository.get_by_name.return_value = mock_product

        result = self.product_service.get_product(product_name)

        self.mock_repository.get_by_name.assert_called_once_with(product_name)
        self.assertEqual(result, mock_product)

    def test_get_product_not_found(self):
        """Тест get_product выбрасывает ProductNotFoundError, если продукт не найден."""
        product_name = "Nonexistent Product"
        self.mock_repository.get_by_name.return_value = None

        with self.assertRaisesRegex(
            ProductNotFoundError, f"Product '{product_name}' is not found"
        ):
            self.product_service.get_product(product_name)

        self.mock_repository.get_by_name.assert_called_once_with(product_name)

    def test_update_product_found(self):
        """Тест update_product обновляет продукт, если найден."""
        product_name = "Product To Update"
        new_product_data = {"name": "Updated Product", "price": 120}
        mock_existing_product = {"id": 2, "name": product_name, "price": 100}
        mock_updated_product = {"id": 2, **new_product_data}

        self.mock_repository.get_by_name.return_value = mock_existing_product
        self.mock_repository.update.return_value = mock_updated_product

        result = self.product_service.update_product(product_name, new_product_data)

        self.mock_repository.get_by_name.assert_called_once_with(product_name)
        self.mock_repository.update.assert_called_once_with(
            product_name, new_product_data
        )
        self.assertEqual(result, mock_updated_product)

    def test_update_product_not_found(self):
        """Тест update_product выбрасывает ProductNotFoundError, если продукт не найден."""
        product_name = "Product Not Found"
        new_product_data = {"name": "Updated Product", "price": 120}

        self.mock_repository.get_by_name.return_value = None

        with self.assertRaisesRegex(
            ProductNotFoundError, f"Product with name {product_name} is not found"
        ):
            self.product_service.update_product(product_name, new_product_data)

        self.mock_repository.get_by_name.assert_called_once_with(product_name)
        self.mock_repository.update.assert_not_called()

    def test_delete_product_found(self):
        """Тест delete_product удаляет продукт, если найден."""
        product_id = 3
        mock_product = {"id": product_id, "name": "Product to Delete", "price": 200}

        self.mock_repository.get_by_id.return_value = mock_product

        result = self.product_service.delete_product(product_id)

        self.mock_repository.get_by_id.assert_called_once_with(product_id)
        self.mock_repository.delete.assert_called_once_with(product_id)
        self.assertIsNone(result)

    def test_delete_product_not_found(self):
        """Тест delete_product выбрасывает ProductNotFoundError, если продукт не найден."""
        product_id = 4

        self.mock_repository.get_by_id.return_value = None

        with self.assertRaisesRegex(
            ProductNotFoundError, f"Product with id {product_id} is not found"
        ):
            self.product_service.delete_product(product_id)

        self.mock_repository.get_by_id.assert_called_once_with(product_id)
        self.mock_repository.delete.assert_not_called()

    def test_list_products_without_filters(self):
        """Тест list_products без фильтров вызывает get_list репозитория без аргументов."""
        mock_product_list = [{"id": 1, "name": "A"}, {"id": 2, "name": "B"}]
        self.mock_repository.get_list.return_value = mock_product_list

        result = self.product_service.list_products()

        self.mock_repository.get_list.assert_called_once_with(
            limit=None, offset=None, sort_field=None, sort_order=None
        )
        self.assertEqual(result, mock_product_list)

    def test_list_products_with_pagination_and_sorting(self):
        """Тест list_products с пагинацией и сортировкой."""
        mock_product_list = [{"id": 3, "name": "C"}, {"id": 4, "name": "D"}]
        filters = {"limit": 10, "offset": 20, "sort_field": "name", "sort_order": "asc"}
        self.mock_repository.get_list.return_value = mock_product_list

        result = self.product_service.list_products(**filters)

        self.mock_repository.get_list.assert_called_once_with(
            limit=10, offset=20, sort_field="name", sort_order="asc"
        )
        self.assertEqual(result, mock_product_list)

    def test_list_products_with_additional_filters(self):
        """Тест list_products с дополнительными фильтрами."""
        mock_product_list = [{"id": 5, "name": "E", "category": "Electronics"}]
        filters = {"category": "Electronics", "is_active": True}
        self.mock_repository.get_list.return_value = mock_product_list

        result = self.product_service.list_products(**filters)

        self.mock_repository.get_list.assert_called_once_with(
            limit=None,
            offset=None,
            sort_field=None,
            sort_order=None,
            category="Electronics",
            is_active=True,
        )
        self.assertEqual(result, mock_product_list)

    def test_list_products_with_all_filters(self):
        """Тест list_products со всеми возможными фильтрами."""
        mock_product_list = [{"id": 6, "name": "F", "price": 150, "in_stock": True}]
        filters = {
            "limit": 5,
            "offset": 10,
            "sort_field": "price",
            "sort_order": "desc",
            "price_gt": 100,
            "in_stock": True,
        }
        self.mock_repository.get_list.return_value = mock_product_list

        result = self.product_service.list_products(**filters)

        self.mock_repository.get_list.assert_called_once_with(
            limit=5,
            offset=10,
            sort_field="price",
            sort_order="desc",
            price_gt=100,
            in_stock=True,
        )
        self.assertEqual(result, mock_product_list)


if __name__ == "__main__":
    unittest.main(argv=["first-arg-is-ignored"], exit=False)
