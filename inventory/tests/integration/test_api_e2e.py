import json

from inventory.tests.integration.base import MongoIntegrationTestCase


class ApiE2ETests(MongoIntegrationTestCase):
    """
    End-to-end API integration tests hitting real Django views + real MongoDB via MongoEngine.

    Prereq: local MongoDB running (e.g. `docker compose up -d mongo`)
    Run with:
      $env:MONGO_DB_NAME="inventory_test_db"
    """

    def test_category_and_product_end_to_end(self):
        # Create category
        resp = self.client.post(
            "/api/categories/",
            data=json.dumps({"title": "Electronics"}),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, 201, resp.content)
        category_id = resp.json()["id"]

        # List categories
        resp = self.client.get("/api/categories/list/")
        self.assertEqual(resp.status_code, 200)
        titles = {c["title"] for c in resp.json()["categories"]}
        self.assertIn("Electronics", titles)

        # Create product
        resp = self.client.post(
            "/api/products/",
            data=json.dumps(
                {
                    "name": "USB-C Cable",
                    "brand": "CableCo",
                    "price": 199.0,
                    "quantity": 3,
                    "category": category_id,
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, 201, resp.content)
        product_id = resp.json()["id"]

        # List products
        resp = self.client.get("/api/products/list/?page=1&limit=50")
        self.assertEqual(resp.status_code, 200, resp.content)
        ids = {p["id"] for p in resp.json()["products"]}
        self.assertIn(product_id, ids)

        # Update product (endpoint accepts POST in current controller)
        resp = self.client.post(
            f"/api/products/{product_id}/",
            # Service validation requires category even on update in current implementation.
            data=json.dumps({"name": "USB-C Cable (2m)", "category": category_id}),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, 200, resp.content)

        # Add product to category
        resp = self.client.post(f"/api/categories/{category_id}/products/{product_id}/add/")
        self.assertEqual(resp.status_code, 200, resp.content)
        self.assertEqual(resp.json()["category_id"], category_id)

        # List products by category
        resp = self.client.get(f"/api/categories/{category_id}/products/")
        self.assertEqual(resp.status_code, 200, resp.content)
        ids = {p["id"] for p in resp.json()["products"]}
        self.assertIn(product_id, ids)

        # Remove product from category
        resp = self.client.delete(f"/api/categories/{category_id}/products/{product_id}/remove/")
        self.assertEqual(resp.status_code, 200, resp.content)
        self.assertIsNone(resp.json()["category_id"])

        # Soft delete product
        resp = self.client.post(f"/api/products/delete/{product_id}/")
        self.assertEqual(resp.status_code, 200, resp.content)

        # Verify not listed anymore
        resp = self.client.get("/api/products/list/?page=1&limit=50")
        self.assertEqual(resp.status_code, 200, resp.content)
        ids = {p["id"] for p in resp.json()["products"]}
        self.assertNotIn(product_id, ids)

