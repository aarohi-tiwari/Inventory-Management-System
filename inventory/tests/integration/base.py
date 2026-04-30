import os

from django.test import Client, TestCase

from inventory.db import connect_mongo
from inventory.testing import SEED_PROFILES, require_test_mongo_db, teardown_test_mongodb


class MongoIntegrationTestCase(TestCase):
    """
    Base class for integration tests that hit real MongoDB (via MongoEngine).

    Behavior:
    - requires MONGO_DB_NAME (refuses inventory_db)
    - connects to Mongo
    - seeds a deterministic dataset before tests
    - drops the entire Mongo test DB after tests (even if tests fail)

    Seed profile:
    - set env var MONGO_SEED_PROFILE (default: "minimal")
    - available profiles: keys of inventory.testing.SEED_PROFILES
    """

    seed_profile_env = "MONGO_SEED_PROFILE"
    default_seed_profile = "minimal"

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        require_test_mongo_db()
        connect_mongo()

        # Always teardown to prevent leakage (even on failures).
        cls.addClassCleanup(teardown_test_mongodb)

        profile = (os.environ.get(cls.seed_profile_env) or cls.default_seed_profile).strip() or cls.default_seed_profile
        if profile not in SEED_PROFILES:
            raise RuntimeError(
                f"Unknown seed profile {profile!r}. Choose one of: {', '.join(sorted(SEED_PROFILES.keys()))}"
            )

        fn = SEED_PROFILES[profile]
        cls.seed_info = fn()  # type: ignore[call-arg]
        cls.client = Client()

