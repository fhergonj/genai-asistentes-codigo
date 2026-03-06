"""
Comprehensive test suite for Product CRUD API endpoints.

Tests cover:
- GET /products - List all products
- GET /products/{product_id} - Get single product
- POST /products - Create new product
- PUT /products/{product_id} - Update product
- DELETE /products/{product_id} - Delete product

Test organization:
- Tests grouped by endpoint operation in separate classes
- Fixtures for TestClient and database reset
- Coverage of happy paths, validation errors, edge cases, and error conditions
"""

import pytest
from fastapi.testclient import TestClient
from main import app
from database import db


@pytest.fixture
def client():
    """Provide TestClient for API testing."""
    return TestClient(app)


@pytest.fixture
def reset_db():
    """Reset database before each test to ensure clean state."""
    db.reset()
    yield
    db.reset()


class TestListProducts:
    """Tests for GET /products endpoint."""

    def test_list_products_returns_200(self, client, reset_db):
        """Verify that list_products returns 200 status code."""
        response = client.get("/products")
        assert response.status_code == 200

    def test_list_products_returns_list(self, client, reset_db):
        """Verify that list_products returns a list."""
        response = client.get("/products")
        assert isinstance(response.json(), list)

    def test_list_products_contains_sample_data(self, client, reset_db):
        """Verify that list includes sample products from database."""
        response = client.get("/products")
        products = response.json()

        # Should contain at least the sample products
        assert len(products) >= 2

        # Verify sample products exist
        product_titles = [p["title"] for p in products]
        assert "Laptop" in product_titles
        assert "Mouse" in product_titles

    def test_list_products_data_structure(self, client, reset_db):
        """Verify that each product has the correct structure."""
        response = client.get("/products")
        products = response.json()

        for product in products:
            assert "id" in product
            assert "title" in product
            assert "price" in product
            assert isinstance(product["id"], int)
            assert isinstance(product["title"], str)
            assert isinstance(product["price"], (int, float))

    def test_list_products_sample_data_values(self, client, reset_db):
        """Verify that sample products have correct values."""
        response = client.get("/products")
        products = response.json()

        # Find sample products by title
        laptop = next((p for p in products if p["title"] == "Laptop"), None)
        mouse = next((p for p in products if p["title"] == "Mouse"), None)

        assert laptop is not None
        assert laptop["price"] == 999.99
        assert mouse is not None
        assert mouse["price"] == 29.99

    def test_list_products_response_model(self, client, reset_db):
        """Verify that response conforms to ProductRead model."""
        response = client.get("/products")
        data = response.json()

        # Validate response contains list of dicts with required fields
        assert all(isinstance(p, dict) for p in data)
        assert all({"id", "title", "price"}.issubset(p.keys()) for p in data)


class TestGetProduct:
    """Tests for GET /products/{product_id} endpoint."""

    def test_get_product_valid_id_returns_200(self, client, reset_db):
        """Verify that get_product returns 200 for valid product ID."""
        response = client.get("/products/1")
        assert response.status_code == 200

    def test_get_product_valid_id_returns_correct_data(self, client, reset_db):
        """Verify that get_product returns correct product data."""
        response = client.get("/products/1")
        product = response.json()

        assert product["id"] == 1
        assert product["title"] == "Laptop"
        assert product["price"] == 999.99

    def test_get_product_different_valid_id(self, client, reset_db):
        """Verify get_product works with different valid IDs."""
        response = client.get("/products/2")
        product = response.json()

        assert product["id"] == 2
        assert product["title"] == "Mouse"
        assert product["price"] == 29.99

    def test_get_product_invalid_id_returns_404(self, client, reset_db):
        """Verify that get_product returns 404 for non-existent ID."""
        response = client.get("/products/9999")
        assert response.status_code == 404

    def test_get_product_invalid_id_error_message(self, client, reset_db):
        """Verify that 404 error includes meaningful message."""
        product_id = 9999
        response = client.get(f"/products/{product_id}")
        error = response.json()

        assert "detail" in error
        assert f"Product with id {product_id}" in error["detail"]

    def test_get_product_data_structure(self, client, reset_db):
        """Verify that product data has correct structure."""
        response = client.get("/products/1")
        product = response.json()

        assert "id" in product
        assert "title" in product
        assert "price" in product
        assert len(product) == 3  # Only these three fields

    def test_get_product_types_are_correct(self, client, reset_db):
        """Verify that product field types are correct."""
        response = client.get("/products/1")
        product = response.json()

        assert isinstance(product["id"], int)
        assert isinstance(product["title"], str)
        assert isinstance(product["price"], (int, float))

    def test_get_product_zero_id_returns_404(self, client, reset_db):
        """Verify that ID 0 is treated as non-existent."""
        response = client.get("/products/0")
        assert response.status_code == 404

    def test_get_product_negative_id_returns_404(self, client, reset_db):
        """Verify that negative IDs return 404."""
        response = client.get("/products/-1")
        assert response.status_code == 404


class TestCreateProduct:
    """Tests for POST /products endpoint."""

    def test_create_product_success_returns_201(self, client, reset_db):
        """Verify that successful product creation returns 201 status code."""
        payload = {"title": "Keyboard", "price": 79.99}
        response = client.post("/products", json=payload)
        assert response.status_code == 201

    def test_create_product_success_returns_created_data(self, client, reset_db):
        """Verify that created product data is returned."""
        payload = {"title": "Keyboard", "price": 79.99}
        response = client.post("/products", json=payload)
        product = response.json()

        assert product["id"] is not None
        assert product["title"] == "Keyboard"
        assert product["price"] == 79.99

    def test_create_product_assigns_unique_id(self, client, reset_db):
        """Verify that each created product gets a unique ID."""
        payload1 = {"title": "Keyboard", "price": 79.99}
        payload2 = {"title": "Monitor", "price": 299.99}

        response1 = client.post("/products", json=payload1)
        response2 = client.post("/products", json=payload2)

        product1 = response1.json()
        product2 = response2.json()

        assert product1["id"] != product2["id"]

    def test_create_product_persists_to_database(self, client, reset_db):
        """Verify that created product is actually stored."""
        payload = {"title": "Keyboard", "price": 79.99}
        post_response = client.post("/products", json=payload)
        created_id = post_response.json()["id"]

        # Retrieve the product
        get_response = client.get(f"/products/{created_id}")
        assert get_response.status_code == 200
        product = get_response.json()
        assert product["title"] == "Keyboard"
        assert product["price"] == 79.99

    def test_create_product_appears_in_list(self, client, reset_db):
        """Verify that created product appears in list_products."""
        initial_response = client.get("/products")
        initial_count = len(initial_response.json())

        payload = {"title": "Monitor", "price": 299.99}
        client.post("/products", json=payload)

        final_response = client.get("/products")
        final_count = len(final_response.json())

        assert final_count == initial_count + 1

    def test_create_product_missing_title_returns_422(self, client, reset_db):
        """Verify that missing title field returns 422 validation error."""
        payload = {"price": 79.99}
        response = client.post("/products", json=payload)
        assert response.status_code == 422

    def test_create_product_missing_price_returns_422(self, client, reset_db):
        """Verify that missing price field returns 422 validation error."""
        payload = {"title": "Keyboard"}
        response = client.post("/products", json=payload)
        assert response.status_code == 422

    def test_create_product_empty_title_returns_422(self, client, reset_db):
        """Verify that empty title string returns 422 validation error."""
        payload = {"title": "", "price": 79.99}
        response = client.post("/products", json=payload)
        assert response.status_code == 422

    def test_create_product_zero_price_returns_422(self, client, reset_db):
        """Verify that zero price returns 422 validation error."""
        payload = {"title": "Keyboard", "price": 0}
        response = client.post("/products", json=payload)
        assert response.status_code == 422

    def test_create_product_negative_price_returns_422(self, client, reset_db):
        """Verify that negative price returns 422 validation error."""
        payload = {"title": "Keyboard", "price": -10.99}
        response = client.post("/products", json=payload)
        assert response.status_code == 422

    def test_create_product_invalid_price_type_returns_422(self, client, reset_db):
        """Verify that non-numeric price returns 422 validation error."""
        payload = {"title": "Keyboard", "price": "expensive"}
        response = client.post("/products", json=payload)
        assert response.status_code == 422

    def test_create_product_with_whitespace_title_accepted(self, client, reset_db):
        """Verify that title with whitespace is accepted."""
        payload = {"title": "  Wireless Keyboard  ", "price": 79.99}
        response = client.post("/products", json=payload)
        assert response.status_code == 201
        product = response.json()
        assert product["title"] == "  Wireless Keyboard  "

    def test_create_product_decimal_price(self, client, reset_db):
        """Verify that decimal prices are handled correctly."""
        payload = {"title": "Item", "price": 12.5}
        response = client.post("/products", json=payload)
        assert response.status_code == 201
        product = response.json()
        assert product["price"] == 12.5

    def test_create_product_large_price(self, client, reset_db):
        """Verify that large prices are accepted."""
        payload = {"title": "Expensive Item", "price": 99999.99}
        response = client.post("/products", json=payload)
        assert response.status_code == 201
        product = response.json()
        assert product["price"] == 99999.99

    def test_create_product_very_small_price(self, client, reset_db):
        """Verify that very small positive prices are accepted."""
        payload = {"title": "Cheap Item", "price": 0.01}
        response = client.post("/products", json=payload)
        assert response.status_code == 201
        product = response.json()
        assert product["price"] == 0.01

    def test_create_product_long_title(self, client, reset_db):
        """Verify that long titles are accepted."""
        long_title = "A" * 500
        payload = {"title": long_title, "price": 79.99}
        response = client.post("/products", json=payload)
        assert response.status_code == 201
        product = response.json()
        assert product["title"] == long_title

    def test_create_product_special_characters_in_title(self, client, reset_db):
        """Verify that special characters in title are accepted."""
        payload = {"title": "Product & Stuff (Special!)", "price": 79.99}
        response = client.post("/products", json=payload)
        assert response.status_code == 201
        product = response.json()
        assert product["title"] == "Product & Stuff (Special!)"


class TestUpdateProduct:
    """Tests for PUT /products/{product_id} endpoint."""

    def test_update_product_success_returns_200(self, client, reset_db):
        """Verify that successful update returns 200 status code."""
        payload = {"title": "Updated Laptop", "price": 1299.99}
        response = client.put("/products/1", json=payload)
        assert response.status_code == 200

    def test_update_product_success_returns_updated_data(self, client, reset_db):
        """Verify that updated product data is returned."""
        payload = {"title": "Updated Laptop", "price": 1299.99}
        response = client.put("/products/1", json=payload)
        product = response.json()

        assert product["id"] == 1
        assert product["title"] == "Updated Laptop"
        assert product["price"] == 1299.99

    def test_update_product_persists_to_database(self, client, reset_db):
        """Verify that updated product is persisted."""
        payload = {"title": "Updated Laptop", "price": 1299.99}
        client.put("/products/1", json=payload)

        # Retrieve the product to verify update
        response = client.get("/products/1")
        product = response.json()

        assert product["title"] == "Updated Laptop"
        assert product["price"] == 1299.99

    def test_update_product_partial_update_title_only(self, client, reset_db):
        """Verify that only title can be updated while keeping price."""
        original = client.get("/products/1").json()
        original_price = original["price"]

        payload = {"title": "New Title", "price": None}
        response = client.put("/products/1", json=payload)
        product = response.json()

        assert product["title"] == "New Title"
        assert product["price"] == original_price

    def test_update_product_partial_update_price_only(self, client, reset_db):
        """Verify that only price can be updated while keeping title."""
        original = client.get("/products/1").json()
        original_title = original["title"]

        payload = {"title": None, "price": 1599.99}
        response = client.put("/products/1", json=payload)
        product = response.json()

        assert product["title"] == original_title
        assert product["price"] == 1599.99

    def test_update_product_partial_update_no_fields(self, client, reset_db):
        """Verify that partial update with no fields preserves original data."""
        original = client.get("/products/1").json()

        payload = {"title": None, "price": None}
        response = client.put("/products/1", json=payload)
        product = response.json()

        assert product["title"] == original["title"]
        assert product["price"] == original["price"]

    def test_update_product_nonexistent_id_returns_404(self, client, reset_db):
        """Verify that updating non-existent product returns 404."""
        payload = {"title": "Updated", "price": 99.99}
        response = client.put("/products/9999", json=payload)
        assert response.status_code == 404

    def test_update_product_nonexistent_id_error_message(self, client, reset_db):
        """Verify that 404 error includes meaningful message."""
        product_id = 9999
        payload = {"title": "Updated", "price": 99.99}
        response = client.put(f"/products/{product_id}", json=payload)
        error = response.json()

        assert "detail" in error
        assert f"Product with id {product_id}" in error["detail"]

    def test_update_product_invalid_price_returns_422(self, client, reset_db):
        """Verify that invalid price returns 422 validation error."""
        payload = {"title": "Updated", "price": -50.0}
        response = client.put("/products/1", json=payload)
        assert response.status_code == 422

    def test_update_product_zero_price_returns_422(self, client, reset_db):
        """Verify that zero price returns 422 validation error."""
        payload = {"title": "Updated", "price": 0}
        response = client.put("/products/1", json=payload)
        assert response.status_code == 422

    def test_update_product_empty_title_returns_422(self, client, reset_db):
        """Verify that empty title returns 422 validation error."""
        payload = {"title": "", "price": 99.99}
        response = client.put("/products/1", json=payload)
        assert response.status_code == 422

    def test_update_product_invalid_price_type_returns_422(self, client, reset_db):
        """Verify that non-numeric price returns 422 validation error."""
        payload = {"title": "Updated", "price": "expensive"}
        response = client.put("/products/1", json=payload)
        assert response.status_code == 422

    def test_update_product_multiple_updates(self, client, reset_db):
        """Verify that product can be updated multiple times."""
        # First update
        payload1 = {"title": "First Update", "price": 500.0}
        response1 = client.put("/products/1", json=payload1)
        assert response1.status_code == 200

        # Second update
        payload2 = {"title": "Second Update", "price": 750.0}
        response2 = client.put("/products/1", json=payload2)
        assert response2.status_code == 200

        # Verify final state
        product = response2.json()
        assert product["title"] == "Second Update"
        assert product["price"] == 750.0

    def test_update_product_preserves_id(self, client, reset_db):
        """Verify that update preserves the product ID."""
        original_id = client.get("/products/1").json()["id"]

        payload = {"title": "Updated", "price": 999.0}
        updated = client.put("/products/1", json=payload).json()

        assert updated["id"] == original_id

    def test_update_product_does_not_affect_other_products(self, client, reset_db):
        """Verify that updating one product doesn't affect others."""
        # Get original state of product 2
        original_product_2 = client.get("/products/2").json()

        # Update product 1
        payload = {"title": "Updated Laptop", "price": 1299.99}
        client.put("/products/1", json=payload)

        # Verify product 2 is unchanged
        updated_product_2 = client.get("/products/2").json()
        assert updated_product_2 == original_product_2

    def test_update_product_with_very_small_price(self, client, reset_db):
        """Verify that very small positive prices are accepted in update."""
        payload = {"title": "Cheap", "price": 0.01}
        response = client.put("/products/1", json=payload)
        assert response.status_code == 200
        product = response.json()
        assert product["price"] == 0.01

    def test_update_product_with_large_price(self, client, reset_db):
        """Verify that large prices are accepted in update."""
        payload = {"title": "Expensive", "price": 999999.99}
        response = client.put("/products/1", json=payload)
        assert response.status_code == 200
        product = response.json()
        assert product["price"] == 999999.99


class TestDeleteProduct:
    """Tests for DELETE /products/{product_id} endpoint."""

    def test_delete_product_success_returns_204(self, client, reset_db):
        """Verify that successful deletion returns 204 status code."""
        response = client.delete("/products/1")
        assert response.status_code == 204

    def test_delete_product_no_response_body(self, client, reset_db):
        """Verify that 204 response has no body."""
        response = client.delete("/products/1")
        assert response.text == ""

    def test_delete_product_actually_removes_product(self, client, reset_db):
        """Verify that product is actually deleted from database."""
        client.delete("/products/1")

        # Try to retrieve deleted product
        response = client.get("/products/1")
        assert response.status_code == 404

    def test_delete_product_removes_from_list(self, client, reset_db):
        """Verify that deleted product is removed from list."""
        initial_response = client.get("/products")
        initial_count = len(initial_response.json())

        client.delete("/products/1")

        final_response = client.get("/products")
        final_count = len(final_response.json())

        assert final_count == initial_count - 1

    def test_delete_product_nonexistent_id_returns_404(self, client, reset_db):
        """Verify that deleting non-existent product returns 404."""
        response = client.delete("/products/9999")
        assert response.status_code == 404

    def test_delete_product_nonexistent_id_error_message(self, client, reset_db):
        """Verify that 404 error includes meaningful message."""
        product_id = 9999
        response = client.delete(f"/products/{product_id}")
        error = response.json()

        assert "detail" in error
        assert f"Product with id {product_id}" in error["detail"]

    def test_delete_product_does_not_affect_other_products(self, client, reset_db):
        """Verify that deleting one product doesn't affect others."""
        # Get original state of product 2
        original_product_2 = client.get("/products/2").json()

        # Delete product 1
        client.delete("/products/1")

        # Verify product 2 still exists with same data
        updated_product_2 = client.get("/products/2").json()
        assert updated_product_2 == original_product_2

    def test_delete_product_twice_returns_404(self, client, reset_db):
        """Verify that deleting the same product twice fails second time."""
        # First deletion should succeed
        response1 = client.delete("/products/1")
        assert response1.status_code == 204

        # Second deletion should fail with 404
        response2 = client.delete("/products/1")
        assert response2.status_code == 404

    def test_delete_product_can_be_recreated(self, client, reset_db):
        """Verify that deleted product ID can be reused after creation."""
        # Delete product 1
        client.delete("/products/1")

        # Create new product - should get a new ID
        payload = {"title": "New Product", "price": 99.99}
        response = client.post("/products", json=payload)
        new_id = response.json()["id"]

        # New product should not have the deleted ID (depends on implementation)
        # Just verify we can create a new product after deletion
        assert new_id is not None

    def test_delete_product_removes_only_target(self, client, reset_db):
        """Verify that only the target product is deleted."""
        # Get all products
        initial_products = client.get("/products").json()
        initial_count = len(initial_products)

        # Delete product with ID 1
        client.delete("/products/1")

        # Get remaining products
        remaining_products = client.get("/products").json()
        remaining_count = len(remaining_products)

        # Verify count decreased by 1
        assert remaining_count == initial_count - 1

        # Verify product 1 is not in remaining products
        product_ids = [p["id"] for p in remaining_products]
        assert 1 not in product_ids

    def test_delete_product_zero_id_returns_404(self, client, reset_db):
        """Verify that deleting product with ID 0 returns 404."""
        response = client.delete("/products/0")
        assert response.status_code == 404

    def test_delete_product_negative_id_returns_404(self, client, reset_db):
        """Verify that deleting product with negative ID returns 404."""
        response = client.delete("/products/-1")
        assert response.status_code == 404


class TestOpenAPI:
    """Tests for API documentation endpoints."""

    def test_openapi_documentation_available(self, client):
        """Verify that OpenAPI documentation is available."""
        response = client.get("/openapi.json")
        assert response.status_code == 200

    def test_openapi_has_product_endpoints(self, client):
        """Verify that OpenAPI includes product endpoints."""
        response = client.get("/openapi.json")
        openapi = response.json()

        # Check that paths exist for product endpoints
        paths = openapi.get("paths", {})
        assert "/products" in paths
        assert "/products/{product_id}" in paths

    def test_swagger_ui_available(self, client):
        """Verify that Swagger UI is available."""
        response = client.get("/docs")
        assert response.status_code == 200

    def test_redoc_available(self, client):
        """Verify that ReDoc is available."""
        response = client.get("/redoc")
        assert response.status_code == 200


class TestIntegration:
    """Integration tests for complete workflows."""

    def test_complete_crud_workflow(self, client, reset_db):
        """Test complete create, read, update, delete workflow."""
        # Create
        create_payload = {"title": "Test Product", "price": 99.99}
        create_response = client.post("/products", json=create_payload)
        assert create_response.status_code == 201
        product_id = create_response.json()["id"]

        # Read
        read_response = client.get(f"/products/{product_id}")
        assert read_response.status_code == 200
        product = read_response.json()
        assert product["title"] == "Test Product"
        assert product["price"] == 99.99

        # Update
        update_payload = {"title": "Updated Product", "price": 149.99}
        update_response = client.put(f"/products/{product_id}", json=update_payload)
        assert update_response.status_code == 200
        updated = update_response.json()
        assert updated["title"] == "Updated Product"
        assert updated["price"] == 149.99

        # Delete
        delete_response = client.delete(f"/products/{product_id}")
        assert delete_response.status_code == 204

        # Verify deletion
        final_response = client.get(f"/products/{product_id}")
        assert final_response.status_code == 404

    def test_multiple_products_workflow(self, client, reset_db):
        """Test creating and managing multiple products."""
        products_data = [
            {"title": "Product A", "price": 10.0},
            {"title": "Product B", "price": 20.0},
            {"title": "Product C", "price": 30.0},
        ]

        created_ids = []
        for data in products_data:
            response = client.post("/products", json=data)
            assert response.status_code == 201
            created_ids.append(response.json()["id"])

        # Verify all products in list
        list_response = client.get("/products")
        all_products = list_response.json()
        assert len(all_products) >= 5  # 2 sample + 3 new

        # Delete one and verify
        client.delete(f"/products/{created_ids[0]}")
        list_response = client.get("/products")
        all_products = list_response.json()
        assert len(all_products) == 4

    def test_error_recovery_workflow(self, client, reset_db):
        """Test that API recovers properly from validation errors."""
        # Send invalid request
        invalid_payload = {"title": "", "price": -10}
        response = client.post("/products", json=invalid_payload)
        assert response.status_code == 422

        # Verify API still works
        valid_payload = {"title": "Valid Product", "price": 99.99}
        response = client.post("/products", json=valid_payload)
        assert response.status_code == 201

    def test_concurrent_operations(self, client, reset_db):
        """Test multiple sequential operations work correctly."""
        # Create two products
        id1 = client.post("/products", json={"title": "Product 1", "price": 100.0}).json()["id"]
        id2 = client.post("/products", json={"title": "Product 2", "price": 200.0}).json()["id"]

        # Update first product
        client.put(f"/products/{id1}", json={"title": "Updated 1", "price": 150.0})

        # Delete second product
        client.delete(f"/products/{id2}")

        # Create new product
        id3 = client.post("/products", json={"title": "Product 3", "price": 300.0}).json()["id"]

        # Verify final state
        products = client.get("/products").json()
        assert any(p["id"] == id1 and p["title"] == "Updated 1" for p in products)
        assert not any(p["id"] == id2 for p in products)
        assert any(p["id"] == id3 for p in products)
