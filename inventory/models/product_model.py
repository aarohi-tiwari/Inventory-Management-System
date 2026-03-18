from mongoengine import Document, StringField, FloatField, IntField, BooleanField, DateTimeField

class Product(Document):
    name = StringField(required=True)
    description = StringField()
    category = StringField()
    price = FloatField(required=True)
    brand = StringField()
    quantity = IntField(default=0)
    is_deleted = BooleanField(default=False)  # Soft delete
    #  AUDIT FIELDS
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)