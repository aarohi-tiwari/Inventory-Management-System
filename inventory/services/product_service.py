from inventory.repositories.product_repository import ProductRepository
from inventory.models.product_category_model import ProductCategory
from datetime import datetime
from bson import ObjectId

class ProductService:

    @staticmethod
    def _normalize_payload(data):
        """Form sends category \"\" for 'no category'; MongoEngine needs None."""
        out = dict(data)
        if "category" in out:
            c = out["category"]
            if c is None or c == "":
                out["category"] = None
            elif isinstance(c, str):
                s = c.strip()
                out["category"] = s if s else None
        return out

    @staticmethod
    def _materialize_category(data):
        """
        ReferenceField accepts DBRef, ObjectId, or the referenced Document.
        Raw strings often fail on setattr() during updates; use the document instance.
        """
        out = dict(data)
        if "category" not in out:
            return out
        c = out["category"]
        if c is None:
            return out
        if isinstance(c, ProductCategory):
            return out
        if isinstance(c, str):
            sid = c.strip()
            if not sid:
                out["category"] = None
                return out
            qid = ObjectId(sid) if ObjectId.is_valid(sid) else sid
            doc = ProductCategory.objects(id=qid).first()
            if doc:
                out["category"] = doc
        return out

    @staticmethod
    def parse_iso_datetime(value, field_name):
        if not value:
            return None, None
        try:
            normalized = value.replace("Z", "+00:00")
            return datetime.fromisoformat(normalized), None
        except ValueError:
            return None, f"{field_name} must be a valid ISO datetime"

    @staticmethod
    def validate(data, is_create=False):
        errors = {}

        if is_create and not data.get("brand"):
            errors["brand"] = "Brand is required"
        elif "brand" in data and not data.get("brand"):
            errors["brand"] = "Brand cannot be empty"

        if not data.get("category"):
            errors["category"] = "Category is required"
        else:
            raw = data["category"]
            if isinstance(raw, ProductCategory):
                pass
            else:
                sid = str(raw).strip()
                if not sid:
                    errors["category"] = "Category is required"
                else:
                    qid = ObjectId(sid) if ObjectId.is_valid(sid) else sid
                    category = ProductCategory.objects(id=qid).first()
                    if not category:
                        errors["category"] = "Invalid category ID"

        if "name" in data and not data.get("name"):
            errors["name"] = "Name is required"

        if "price" in data and data["price"] < 0:
            errors["price"] = "Price must be positive"

        if "quantity" in data and data["quantity"] < 0:
            errors["quantity"] = "Quantity cannot be negative"

        return errors

    @staticmethod
    def create_product(data):
        data = ProductService._normalize_payload(data)
        errors = ProductService.validate(data, is_create=True)
        if errors:
            return None, errors

        data = ProductService._materialize_category(data)
        return ProductRepository.create(data), None

    @staticmethod
    def get_products(page, limit, search=None, brand=None, category=None, created_after=None, updated_after=None, sort_by="-created_at"):
        created_after_dt, created_after_error = ProductService.parse_iso_datetime(created_after, "created_after")
        updated_after_dt, updated_after_error = ProductService.parse_iso_datetime(updated_after, "updated_after")

        errors = {}
        if created_after_error:
            errors["created_after"] = created_after_error
        if updated_after_error:
            errors["updated_after"] = updated_after_error
        if errors:
            return None, None, None, errors

        products, total, total_pages = ProductRepository.get_all(
            page, limit, search, brand, category, created_after_dt, updated_after_dt, sort_by
        )
        return products, total, total_pages, None
    
    @staticmethod
    def update_product(product_id, data):
        data = ProductService._normalize_payload(data)
        errors = ProductService.validate(data, is_create=False)
        if errors:
            return None, errors

        data = ProductService._materialize_category(data)
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