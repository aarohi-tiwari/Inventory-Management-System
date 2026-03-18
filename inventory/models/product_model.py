from mongoengine import Document, StringField, FloatField, IntField, BooleanField

class Product(Document):
    name = StringField(required=True)
    description = StringField()
    category = StringField()
    price = FloatField(required=True)
    brand = StringField()
    quantity = IntField(default=0)
    is_deleted = BooleanField(default=False)  # ✅ Soft delete