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


def backfill_missing_brands(default_brand=None, dry_run=True):
    missing = Product.objects(brand__in=[None, ""])
    count = missing.count()

    if dry_run:
        print(f"Found {count} product(s) with missing brand.")
        return

    if not default_brand:
        print("default_brand is required when dry_run is False")
        return

    updated = 0
    for product in missing:
        product.brand = default_brand
        product.save()
        updated += 1

    print(f"Updated {updated} product(s) with default brand '{default_brand}'.")


if __name__ == "__main__":
    # 1) report only:
    backfill_missing_brands(dry_run=True)
    # 2) uncomment this to apply:
    # backfill_missing_brands(default_brand="Unknown", dry_run=False)
