import os
import sys

# Add project root to path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django
django.setup()

"""
Deprecated.

Use the Django management command instead:
  py manage.py cleanup_category_old
"""

if __name__ == "__main__":
    raise SystemExit("Deprecated: run `py manage.py cleanup_category_old` instead.")