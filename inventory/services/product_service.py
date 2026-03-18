from inventory.repositories.product_repository import ProductRepository

class ProductService:

    @staticmethod
    def validate(data):
        errors = {}

        if "name" in data and not data.get("name"):
            errors["name"] = "Name is required"

        if "price" in data and data["price"] < 0:
            errors["price"] = "Price must be positive"

        if "quantity" in data and data["quantity"] < 0:
            errors["quantity"] = "Quantity cannot be negative"

        return errors

    @staticmethod
    def create_product(data):
        errors = ProductService.validate(data)
        if errors:
            return None, errors

        return ProductRepository.create(data), None

    @staticmethod
    def get_products(page, limit, search=None, brand=None, category=None):
        return ProductRepository.get_all(page, limit, search, brand, category)
    
    @staticmethod
    def update_product(product_id, data):
        errors = ProductService.validate(data)
        if errors:
            return None, errors

        product = ProductRepository.update(product_id, data)
        if not product:
            return None, {"error": "Product not found"}

        return product, None

    @staticmethod
    def delete_product(product_id):
        success = ProductRepository.soft_delete(product_id)
        if not success:
            return {"error": "Product not found"}
        return None