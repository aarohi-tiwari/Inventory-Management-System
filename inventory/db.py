import os
from mongoengine import connect


def connect_mongo():
    db_name = os.environ.get("MONGO_DB_NAME", "inventory_db")
    host = os.environ.get("MONGO_HOST", "localhost")
    port = int(os.environ.get("MONGO_PORT", "27017"))
    return connect(db=db_name, host=host, port=port)


# Preserve existing behavior (connect on import), but allow env overrides.
connect_mongo()