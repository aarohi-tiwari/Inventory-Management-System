from datetime import datetime, timezone
from mongoengine import Document, StringField, DateTimeField

class ProductCategory(Document):
    meta = {"strict": False}

    title = StringField(required=True, unique=True)

    created_at = DateTimeField()
    updated_at = DateTimeField()

    def save(self, *args, **kwargs):
        now = datetime.now(timezone.utc)
        if not self.created_at:
            self.created_at = now
        self.updated_at = now
        return super().save(*args, **kwargs)