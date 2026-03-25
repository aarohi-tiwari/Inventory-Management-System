from inventory.models.product_model import Product
from django.core.paginator import Paginator

class ProductRepository:

    @staticmethod
    def create(data):
        product = Product(**data)
        product.save()
        return product

    @staticmethod
    def get_by_id(product_id):
        return Product.objects(id=product_id, is_deleted=False).first()

    @staticmethod
    def get_all(page, limit, search=None, brand=None, category=None, created_after=None, updated_after=None, sort_by="-created_at"):
        products = Product.objects.filter(is_deleted=False)

        if search:
            products = products.filter(name__icontains=search)

        if brand:
            products = products.filter(brand__icontains=brand)

        if category:
            products = products.filter(category=category)

        if created_after:
            products = products.filter(created_at__gte=created_after)

        if updated_after:
            products = products.filter(updated_at__gte=updated_after)

        allowed_sorts = {"created_at", "-created_at", "updated_at", "-updated_at", "name", "-name"}
        if sort_by in allowed_sorts:
            products = products.order_by(sort_by)

        total = products.count()

        paginator = Paginator(products, limit)
        page_obj = paginator.get_page(page)

        return page_obj, total, paginator.num_pages

    @staticmethod
    def update(product_id, data):
        product = Product.objects(id=product_id, is_deleted=False).first()
        if not product:
            return None

        for key, value in data.items():
            setattr(product, key, value)

        product.save()
        return product

    @staticmethod
    def soft_delete(product_id):
        product = Product.objects(id=product_id).first()
        if not product:
            return False

        product.is_deleted = True
        product.save()
        return True

    @staticmethod
    def get_products_by_category(category_id):
        return Product.objects(category=category_id, is_deleted=False)

    @staticmethod
    def assign_category(product_id, category):
        product = Product.objects(id=product_id, is_deleted=False).first()
        if not product:
            return None
        product.category = category
        product.save()
        return product

    @staticmethod
    def remove_category(product_id, category_id):
        product = Product.objects(id=product_id, is_deleted=False, category=category_id).first()
        if not product:
            return None
        product.category = None
        product.save()
        return product