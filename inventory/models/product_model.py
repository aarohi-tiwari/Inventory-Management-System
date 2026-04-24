from datetime import datetime, timezone
from mongoengine import Document, StringField, FloatField, IntField, BooleanField, DateTimeField
from mongoengine import ReferenceField
from inventory.models.product_category_model import ProductCategory

class Product(Document):
    meta = {"strict": False}

    name = StringField(required=True)
    category = ReferenceField(ProductCategory)
    category_old = StringField()   # TEMP
    price = FloatField(required=True)
    brand = StringField()
    quantity = IntField(default=0, min_value=0) 

    # price = DecimalField(max_digits=10, decimal_places=2)
    # quantity = PositiveIntegerField()

    is_deleted = BooleanField(default=False)  # Soft delete
    # Audit fields
    created_at = DateTimeField()
    updated_at = DateTimeField()

    def save(self, *args, **kwargs):
        now = datetime.now(timezone.utc)
        if not self.created_at:
            self.created_at = now
        self.updated_at = now
        return super().save(*args, **kwargs)