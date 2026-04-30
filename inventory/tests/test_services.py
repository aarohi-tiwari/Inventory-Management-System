from django.test import SimpleTestCase
from unittest.mock import MagicMock, patch


class ProductServiceTests(SimpleTestCase):
    def test_parse_iso_datetime_empty_returns_none(self):
        from inventory.services.product_service import ProductService

        dt, err = ProductService.parse_iso_datetime("", "created_after")
        self.assertIsNone(dt)
        self.assertIsNone(err)

    def test_parse_iso_datetime_invalid_returns_error(self):
        from inventory.services.product_service import ProductService

        dt, err = ProductService.parse_iso_datetime("not-a-date", "created_after")
        self.assertIsNone(dt)
        self.assertEqual(err, "created_after must be a valid ISO datetime")

    @patch("inventory.services.product_service.ProductCategory.objects")
    def test_validate_requires_category_and_checks_existence(self, objects_mock):
        from inventory.services.product_service import ProductService

        objects_mock.return_value.first.return_value = None
        errors = ProductService.validate({"brand": "B", "category": "507f1f77bcf86cd799439011"}, is_create=True)
        self.assertEqual(errors.get("category"), "Invalid category ID")

    @patch("inventory.services.product_service.ProductRepository")
    @patch("inventory.services.product_service.ProductCategory.objects")
    def test_create_product_success_materializes_category_and_calls_repo(self, objects_mock, ProductRepositoryMock):
        from inventory.services.product_service import ProductService

        category_doc = MagicMock(name="category_doc")
        objects_mock.return_value.first.return_value = category_doc
        ProductRepositoryMock.create.return_value = {"_id": "p1"}

        product, errors = ProductService.create_product(
            {"brand": "Brand", "category": "507f1f77bcf86cd799439011", "name": "N", "price": 1, "quantity": 2}
        )

        self.assertIsNone(errors)
        self.assertEqual(product, {"_id": "p1"})
        ProductRepositoryMock.create.assert_called_once()
        called_payload = ProductRepositoryMock.create.call_args.args[0]
        self.assertIs(called_payload["category"], category_doc)

    @patch("inventory.services.product_service.ProductRepository")
    def test_create_product_validation_errors_do_not_call_repo(self, ProductRepositoryMock):
        from inventory.services.product_service import ProductService

        product, errors = ProductService.create_product({"brand": "", "category": ""})
        self.assertIsNone(product)
        self.assertIn("brand", errors)
        self.assertIn("category", errors)
        ProductRepositoryMock.create.assert_not_called()

    @patch("inventory.services.product_service.ProductRepository")
    def test_get_products_invalid_dates_returns_errors(self, ProductRepositoryMock):
        from inventory.services.product_service import ProductService

        products, total, total_pages, errors = ProductService.get_products(
            page=1,
            limit=10,
            created_after="bad",
            updated_after="also-bad",
        )
        self.assertIsNone(products)
        self.assertIsNone(total)
        self.assertIsNone(total_pages)
        self.assertEqual(errors["created_after"], "created_after must be a valid ISO datetime")
        self.assertEqual(errors["updated_after"], "updated_after must be a valid ISO datetime")
        ProductRepositoryMock.get_all.assert_not_called()

    @patch("inventory.services.product_service.ProductRepository")
    @patch("inventory.services.product_service.ProductCategory.objects")
    def test_update_product_not_found_returns_error(self, objects_mock, ProductRepositoryMock):
        from inventory.services.product_service import ProductService

        objects_mock.return_value.first.return_value = MagicMock(name="category_doc")
        ProductRepositoryMock.update.return_value = None
        product, errors = ProductService.update_product("missing", {"category": "507f1f77bcf86cd799439011"})
        self.assertIsNone(product)
        self.assertEqual(errors, {"error": "Product not found"})

    @patch("inventory.services.product_service.ProductRepository")
    def test_delete_product_not_found_returns_error(self, ProductRepositoryMock):
        from inventory.services.product_service import ProductService

        ProductRepositoryMock.soft_delete.return_value = False
        err = ProductService.delete_product("missing")
        self.assertEqual(err, {"error": "Product not found"})


class ProductCategoryServiceTests(SimpleTestCase):
    @patch("inventory.services.product_category_service.ProductCategoryRepository")
    def test_create_category_validation_error(self, ProductCategoryRepositoryMock):
        from inventory.services.product_category_service import ProductCategoryService

        category, errors = ProductCategoryService.create_category({"title": ""})
        self.assertIsNone(category)
        self.assertEqual(errors, {"title": "Title is required"})
        ProductCategoryRepositoryMock.create.assert_not_called()

    @patch("inventory.services.product_category_service.ProductCategoryRepository")
    def test_get_category_not_found(self, ProductCategoryRepositoryMock):
        from inventory.services.product_category_service import ProductCategoryService

        ProductCategoryRepositoryMock.get_by_id.return_value = None
        category, errors = ProductCategoryService.get_category("missing")
        self.assertIsNone(category)
        self.assertEqual(errors, {"error": "Category not found"})

    @patch("inventory.services.product_category_service.ProductCategoryRepository")
    def test_update_category_not_found(self, ProductCategoryRepositoryMock):
        from inventory.services.product_category_service import ProductCategoryService

        ProductCategoryRepositoryMock.update.return_value = None
        category, errors = ProductCategoryService.update_category("missing", {"title": "T"})
        self.assertIsNone(category)
        self.assertEqual(errors, {"error": "Category not found"})

    @patch("inventory.services.product_category_service.ProductCategoryRepository")
    def test_delete_category_not_found(self, ProductCategoryRepositoryMock):
        from inventory.services.product_category_service import ProductCategoryService

        ProductCategoryRepositoryMock.delete.return_value = False
        err = ProductCategoryService.delete_category("missing")
        self.assertEqual(err, {"error": "Category not found"})

    @patch("inventory.services.product_category_service.ProductRepository")
    @patch("inventory.services.product_category_service.ProductCategoryRepository")
    def test_list_products_by_category_requires_category(self, ProductCategoryRepositoryMock, ProductRepositoryMock):
        from inventory.services.product_category_service import ProductCategoryService

        ProductCategoryRepositoryMock.get_by_id.return_value = None
        products, errors = ProductCategoryService.list_products_by_category("missing")
        self.assertIsNone(products)
        self.assertEqual(errors, {"error": "Category not found"})
        ProductRepositoryMock.get_products_by_category.assert_not_called()

    @patch("inventory.services.product_category_service.ProductRepository")
    @patch("inventory.services.product_category_service.ProductCategoryRepository")
    def test_add_product_to_category_happy_path(self, ProductCategoryRepositoryMock, ProductRepositoryMock):
        from inventory.services.product_category_service import ProductCategoryService

        category_doc = MagicMock(name="category_doc")
        ProductCategoryRepositoryMock.get_by_id.return_value = category_doc
        ProductRepositoryMock.assign_category.return_value = {"_id": "p1", "category": "c1"}

        product, errors = ProductCategoryService.add_product_to_category("c1", "p1")
        self.assertIsNone(errors)
        self.assertEqual(product, {"_id": "p1", "category": "c1"})
        ProductRepositoryMock.assign_category.assert_called_once_with("p1", category_doc)

    @patch("inventory.services.product_category_service.ProductRepository")
    @patch("inventory.services.product_category_service.ProductCategoryRepository")
    def test_remove_product_from_category_product_missing(self, ProductCategoryRepositoryMock, ProductRepositoryMock):
        from inventory.services.product_category_service import ProductCategoryService

        ProductCategoryRepositoryMock.get_by_id.return_value = MagicMock(name="category_doc")
        ProductRepositoryMock.remove_category.return_value = None

        product, errors = ProductCategoryService.remove_product_from_category("c1", "missing")
        self.assertIsNone(product)
        self.assertEqual(errors, {"error": "Product not found or not in this category"})

