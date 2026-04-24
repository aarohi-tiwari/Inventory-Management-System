from inventory.models.product_category_model import ProductCategory

class ProductCategoryRepository:

    @staticmethod
    def create(data):
        return ProductCategory(**data).save()

    @staticmethod
    def get_all():
        return ProductCategory.objects()

    @staticmethod
    def get_by_id(category_id):
        return ProductCategory.objects(id=category_id).first()

    @staticmethod
    def update(category_id, data):
        category = ProductCategory.objects(id=category_id).first()
        if not category:
            return None
        for key, value in data.items():
            setattr(category, key, value)
        category.save()
        return category

    @staticmethod
    def delete(category_id):
        category = ProductCategory.objects(id=category_id).first()
        if not category:
            return False
        category.delete()
        return True