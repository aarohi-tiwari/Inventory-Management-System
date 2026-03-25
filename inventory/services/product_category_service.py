from inventory.repositories.product_category_repository import ProductCategoryRepository
from inventory.repositories.product_repository import ProductRepository

class ProductCategoryService:

    @staticmethod
    def validate(data):
        errors = {}
        if not data.get("title"):
            errors["title"] = "Title is required"
        return errors

    @staticmethod
    def create_category(data):
        errors = ProductCategoryService.validate(data)
        if errors:
            return None, errors
        return ProductCategoryRepository.create(data), None

    @staticmethod
    def get_categories():
        return ProductCategoryRepository.get_all()

    @staticmethod
    def get_category(category_id):
        category = ProductCategoryRepository.get_by_id(category_id)
        if not category:
            return None, {"error": "Category not found"}
        return category, None

    @staticmethod
    def update_category(category_id, data):
        errors = ProductCategoryService.validate(data)
        if errors:
            return None, errors
        category = ProductCategoryRepository.update(category_id, data)
        if not category:
            return None, {"error": "Category not found"}
        return category, None

    @staticmethod
    def delete_category(category_id):
        deleted = ProductCategoryRepository.delete(category_id)
        if not deleted:
            return {"error": "Category not found"}
        return None

    @staticmethod
    def list_products_by_category(category_id):
        category = ProductCategoryRepository.get_by_id(category_id)
        if not category:
            return None, {"error": "Category not found"}
        products = ProductRepository.get_products_by_category(category_id)
        return products, None

    @staticmethod
    def add_product_to_category(category_id, product_id):
        category = ProductCategoryRepository.get_by_id(category_id)
        if not category:
            return None, {"error": "Category not found"}
        product = ProductRepository.assign_category(product_id, category)
        if not product:
            return None, {"error": "Product not found"}
        return product, None

    @staticmethod
    def remove_product_from_category(category_id, product_id):
        category = ProductCategoryRepository.get_by_id(category_id)
        if not category:
            return None, {"error": "Category not found"}
        product = ProductRepository.remove_category(product_id, category_id)
        if not product:
            return None, {"error": "Product not found or not in this category"}
        return product, None