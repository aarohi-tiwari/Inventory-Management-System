import os
import sys
from datetime import datetime, timezone

# Add project root to path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django
django.setup()

from inventory.models.product_model import Product


def backfill_product_audit_fields():
    now = datetime.now(timezone.utc)
    updated_count = 0

    for product in Product.objects():
        changed = False

        if not product.created_at:
            product.created_at = now
            changed = True

        if not product.updated_at:
            # Keep timestamps consistent for historical records
            product.updated_at = product.created_at or now
            changed = True

        if changed:
            product.save()
            updated_count += 1

    print(f"Backfill completed. Updated {updated_count} product(s).")


if __name__ == "__main__":
    backfill_product_audit_fields()
