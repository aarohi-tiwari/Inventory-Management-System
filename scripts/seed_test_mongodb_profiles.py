r"""
Seed the MongoDB *test* database with a chosen deterministic profile.

Usage (PowerShell):
  docker compose up -d mongo
  $env:MONGO_DB_NAME="inventory_test_db"
  .\venv\Scripts\python.exe .\scripts\seed_test_mongodb_profiles.py --profile dataset
  .\venv\Scripts\python.exe .\scripts\seed_test_mongodb_profiles.py --profile pagination --count 50
"""

import argparse
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django  # noqa: E402

django.setup()

from inventory.db import connect_mongo  # noqa: E402
from inventory.testing import (  # noqa: E402
    SEED_PROFILES,
    require_test_mongo_db,
    seed_for_pagination,
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", required=True, choices=sorted(SEED_PROFILES.keys()))
    parser.add_argument("--count", type=int, default=25, help="Only used for profile=pagination")
    args = parser.parse_args()

    require_test_mongo_db()
    connect_mongo()

    if args.profile == "pagination":
        out = seed_for_pagination(count=args.count)
    else:
        fn = SEED_PROFILES[args.profile]
        out = fn()  # type: ignore[call-arg]

    print(f"Seeded DB={os.environ.get('MONGO_DB_NAME')}")
    print(f"profile={args.profile}")
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

