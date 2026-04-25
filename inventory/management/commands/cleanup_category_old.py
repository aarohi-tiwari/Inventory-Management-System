from django.core.management.base import BaseCommand

from inventory.models.product_category_model import ProductCategory
from inventory.models.product_model import Product


class Command(BaseCommand):
    help = "Migrate legacy Product.category_old into Product.category (if needed) and remove category_old from MongoDB."

    def handle(self, *args, **options):
        migrated = 0

        # If some documents still have category_old and category is not set,
        # migrate category_old (string name) -> ProductCategory reference.
        for product in Product.objects(__raw__={"category_old": {"$exists": True, "$ne": ""}}):
            category_old = (product._data.get("category_old") or "").strip()
            if not category_old:
                continue

            if not getattr(product, "category", None):
                title = category_old.title()
                category = ProductCategory.objects(title=title).first()
                if not category:
                    category = ProductCategory(title=title)
                    category.save()

                product.category = category
                product.save()
                migrated += 1

        # Remove the legacy field from all documents where it exists.
        # Use the underlying collection because category_old is no longer a declared field.
        coll = Product._get_collection()
        result = coll.update_many(
            {"category_old": {"$exists": True}},
            {"$unset": {"category_old": ""}},
        )

        self.stdout.write(self.style.SUCCESS(f"Migrated category_old -> category for {migrated} products."))
        self.stdout.write(self.style.SUCCESS(f"Unset category_old for {result.modified_count} documents."))

