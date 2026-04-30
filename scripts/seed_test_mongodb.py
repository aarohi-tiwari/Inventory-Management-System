r"""
Seed a MongoDB database with deterministic inventory data.

Usage (PowerShell):
  docker compose up -d mongo
  $env:MONGO_DB_NAME="inventory_test_db"
  .\venv\Scripts\python.exe .\scripts\seed_test_mongodb.py
"""

import sys
from pathlib import Path
import os

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django  

django.setup()

from inventory.db import connect_mongo  # noqa: E402
from inventory.testing import require_test_mongo_db, seed_test_mongodb  # noqa: E402


if __name__ == "__main__":
    require_test_mongo_db()
    connect_mongo()
    ids = seed_test_mongodb()
    print(f"Seeded DB={os.environ.get('MONGO_DB_NAME', 'inventory_db')}")
    print(ids)

