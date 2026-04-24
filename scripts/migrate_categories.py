import os
import sys

# Add project root to path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django
django.setup()

from inventory.models.product_model import Product
from inventory.models.product_category_model import ProductCategory


def migrate_categories():
    for product in Product.objects():
        if product.category_old:
            category_name = product.category_old.strip().title()

            # Check if category exists
            category = ProductCategory.objects(title=category_name).first()

            if not category:
                category = ProductCategory(title=category_name)
                category.save()

            # Assign reference
            product.category = category
            product.save()

    print("Migration completed ✅")


if __name__ == "__main__":
    migrate_categories()