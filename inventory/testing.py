import os

from mongoengine.connection import get_db

from inventory.db import connect_mongo


class UnsafeTestDatabaseTeardown(RuntimeError):
    pass


def require_test_mongo_db(
    *,
    env_var: str = "MONGO_DB_NAME",
    disallow: tuple[str, ...] = ("inventory_db",),
) -> str:
    name = (os.environ.get(env_var) or "").strip()
    if not name:
        raise UnsafeTestDatabaseTeardown(
            f"{env_var} is not set. In PowerShell run: $env:{env_var}=\"inventory_test_db\""
        )
    if name in disallow:
        raise UnsafeTestDatabaseTeardown(f"Refusing to use disallowed MongoDB database: {name!r}")
    return name


def seed_test_mongodb() -> dict:
    """
    Deterministically seed the Mongo test DB for integration tests.
    Drops collections first to ensure clean state.
    """
    from inventory.models.product_category_model import ProductCategory
    from inventory.models.product_model import Product

    Product.drop_collection()
    ProductCategory.drop_collection()

    groceries = ProductCategory(title="Groceries").save()

    Product(name="Milk 1L", brand="Acme", price=55.0, quantity=10, category=groceries).save()

    return {"groceries_id": str(groceries.id)}


def seed_products_dataset(*, include_electronics: bool = True) -> dict:
    """
    Richer deterministic dataset for list/search/filter/sort/pagination tests.
    Drops collections first to ensure clean state.
    """
    from inventory.models.product_category_model import ProductCategory
    from inventory.models.product_model import Product

    Product.drop_collection()
    ProductCategory.drop_collection()

    groceries = ProductCategory(title="Groceries").save()
    Product(name="Milk 1L", brand="Acme", price=55.0, quantity=10, category=groceries).save()
    Product(name="Bread", brand="BakeCo", price=35.0, quantity=50, category=groceries).save()
    Product(name="Eggs 12-pack", brand="FarmFresh", price=78.0, quantity=20, category=groceries).save()

    electronics = None
    if include_electronics:
        electronics = ProductCategory(title="Electronics").save()
        Product(name="USB-C Cable", brand="CableCo", price=199.0, quantity=25, category=electronics).save()
        Product(name="Keyboard", brand="KeyCo", price=999.0, quantity=5, category=electronics).save()
        Product(name="Mouse", brand="KeyCo", price=499.0, quantity=7, category=electronics).save()

    out = {"groceries_id": str(groceries.id)}
    if electronics:
        out["electronics_id"] = str(electronics.id)
    return out


def seed_with_soft_deleted_products() -> dict:
    """
    Seeds one active and one soft-deleted product to test list filtering.
    Drops collections first.
    """
    from inventory.models.product_category_model import ProductCategory
    from inventory.models.product_model import Product

    Product.drop_collection()
    ProductCategory.drop_collection()

    cat = ProductCategory(title="Groceries").save()
    active = Product(name="Active Item", brand="A", price=10.0, quantity=1, category=cat).save()
    deleted = Product(name="Deleted Item", brand="B", price=20.0, quantity=1, category=cat).save()
    deleted.is_deleted = True
    deleted.save()

    return {"category_id": str(cat.id), "active_id": str(active.id), "deleted_id": str(deleted.id)}


def seed_for_pagination(*, count: int = 25) -> dict:
    """
    Seeds N products in one category for pagination tests.
    Drops collections first.
    """
    from inventory.models.product_category_model import ProductCategory
    from inventory.models.product_model import Product

    Product.drop_collection()
    ProductCategory.drop_collection()

    cat = ProductCategory(title="Groceries").save()
    for i in range(1, count + 1):
        Product(
            name=f"Item {i:03d}",
            brand="SeedBrand",
            price=float(i),
            quantity=i % 7,
            category=cat,
        ).save()

    return {"category_id": str(cat.id), "count": count}


def seed_with_stale_category_reference() -> dict:
    """
    Seeds a product whose category reference points to a deleted category.
    Useful for list API resilience via _safe_category_data().
    Drops collections first.
    """
    from inventory.models.product_category_model import ProductCategory
    from inventory.models.product_model import Product

    Product.drop_collection()
    ProductCategory.drop_collection()

    cat = ProductCategory(title="Temp Category").save()
    p = Product(name="Stale Category Product", brand="Acme", price=1.0, quantity=1, category=cat).save()
    cat_id = str(cat.id)
    cat.delete()  # leaves a stale reference

    return {"deleted_category_id": cat_id, "product_id": str(p.id)}


def seed_full_test_dataset() -> dict:
    """
    Larger deterministic dataset intended for broader integration testing.
    Includes multiple categories, varied brands/prices/quantities, a product without category,
    and a soft-deleted product.
    Drops collections first.
    """
    from inventory.models.product_category_model import ProductCategory
    from inventory.models.product_model import Product

    Product.drop_collection()
    ProductCategory.drop_collection()

    groceries = ProductCategory(title="Groceries").save()
    electronics = ProductCategory(title="Electronics").save()
    stationery = ProductCategory(title="Stationery").save()
    apparel = ProductCategory(title="Apparel").save()

    products = []

    products.append(Product(name="Milk 1L", brand="Acme", price=55.0, quantity=10, category=groceries).save())
    products.append(Product(name="Bread", brand="BakeCo", price=35.0, quantity=50, category=groceries).save())
    products.append(Product(name="Eggs 12-pack", brand="FarmFresh", price=78.0, quantity=20, category=groceries).save())
    products.append(Product(name="Basmati Rice 5kg", brand="GrainHouse", price=499.0, quantity=12, category=groceries).save())

    products.append(Product(name="USB-C Cable", brand="CableCo", price=199.0, quantity=25, category=electronics).save())
    products.append(Product(name="Keyboard", brand="KeyCo", price=999.0, quantity=5, category=electronics).save())
    products.append(Product(name="Mouse", brand="KeyCo", price=499.0, quantity=7, category=electronics).save())
    products.append(Product(name="Power Bank 10k", brand="ChargeIt", price=1299.0, quantity=9, category=electronics).save())

    products.append(Product(name="Notebook A5", brand="PaperCo", price=49.0, quantity=100, category=stationery).save())
    products.append(Product(name="Ball Pen Blue", brand="InkWell", price=10.0, quantity=500, category=stationery).save())
    products.append(Product(name="Marker Set", brand="InkWell", price=149.0, quantity=40, category=stationery).save())

    products.append(Product(name="T-Shirt (M)", brand="WearCo", price=399.0, quantity=30, category=apparel).save())
    products.append(Product(name="Jeans (32)", brand="DenimWorks", price=1299.0, quantity=15, category=apparel).save())

    # Edge case: category can be None at model layer (even if service requires it).
    products.append(Product(name="Uncategorized Sample", brand="Misc", price=1.0, quantity=1, category=None).save())

    # Soft-deleted product (should be excluded by list APIs).
    deleted = Product(name="Deleted Sample", brand="Misc", price=2.0, quantity=1, category=groceries).save()
    deleted.is_deleted = True
    deleted.save()

    return {
        "categories": {
            "groceries_id": str(groceries.id),
            "electronics_id": str(electronics.id),
            "stationery_id": str(stationery.id),
            "apparel_id": str(apparel.id),
        },
        "product_ids": [str(p.id) for p in products],
        "deleted_product_id": str(deleted.id),
    }


SEED_PROFILES: dict[str, object] = {
    "minimal": seed_test_mongodb,
    "dataset": seed_products_dataset,
    "full": seed_full_test_dataset,
    "soft_deleted": seed_with_soft_deleted_products,
    "pagination": seed_for_pagination,
    "stale_refs": seed_with_stale_category_reference,
}


def teardown_test_mongodb(
    *,
    db_name: str | None = None,
    env_var: str = "MONGO_DB_NAME",
    disallow: tuple[str, ...] = ("inventory_db",),
) -> None:
    """
    Drop the MongoDB database used for tests to prevent data leakage.

    Safety:
    - requires an explicit db name (via `db_name` or env var)
    - refuses to drop names in `disallow`
    """
    name = (db_name or os.environ.get(env_var) or "").strip()
    if not name:
        raise UnsafeTestDatabaseTeardown(f"{env_var} is not set; refusing to teardown MongoDB.")
    if name in disallow:
        raise UnsafeTestDatabaseTeardown(f"Refusing to teardown disallowed MongoDB database: {name!r}")

    connect_mongo()
    db = get_db()
    # `db.name` should match `name` if connect_mongo() used the env var.
    if db.name != name:
        raise UnsafeTestDatabaseTeardown(
            f"Connected DB name mismatch (connected={db.name!r}, expected={name!r}); refusing teardown."
        )
    db.client.drop_database(db.name)

