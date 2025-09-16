import io
import pytest

def test_create_product_with_image(client):
    # Simular un archivo en memoria
    file_content = b"fake image content"
    file = io.BytesIO(file_content)
    file.name = "test_image.png"

    response = client.post(
        "/products/",
        data={
            "name": "Test Product",
            "description": "A product for testing",
            "price": 9.99,
            "quantity": 5,
        },
        files={"image": ("test_image.png", file, "image/png")},
    )

    assert response.status_code == 200, response.text
    product = response.json()
    assert product["name"] == "Test Product"
    assert product["description"] == "A product for testing"
    assert product["price"] == 9.99
    assert product["quantity"] == 5
    assert "image_url" in product
    assert product["image_url"].startswith("/static/images/")  # validación de URL


def test_list_products_includes_image(client):
    # Primero creamos un producto
    file_content = b"another fake image"
    file = io.BytesIO(file_content)
    file.name = "list_test.png"

    create_response = client.post(
        "/products/",
        data={
            "name": "List Product",
            "description": "To test listing",
            "price": 19.99,
            "quantity": 2,
        },
        files={"image": ("list_test.png", file, "image/png")},
    )

    assert create_response.status_code == 200, create_response.text

    # Ahora probamos el listado
    list_response = client.get("/products/")
    assert list_response.status_code == 200
    products = list_response.json()

    assert isinstance(products, list)
    assert len(products) > 0

    product = products[0]
    assert "name" in product
    assert "image_url" in product
    assert product["image_url"].startswith("/static/images/")


def test_update_product(client):
    # Primero creamos un producto para actualizar
    file_content = b"original image"
    file = io.BytesIO(file_content)
    file.name = "original.png"

    create_response = client.post(
        "/products/",
        data={
            "name": "Original Product",
            "description": "Original description",
            "price": 10.0,
            "quantity": 5,
        },
        files={"image": ("original.png", file, "image/png")},
    )
    assert create_response.status_code == 200
    product_id = create_response.json()["id"]
    original_image_url = create_response.json()["image_url"]

    # Test 1: Actualización completa (incluyendo nueva imagen)
    new_file_content = b"new image content"
    new_file = io.BytesIO(new_file_content)
    new_file.name = "updated.png"

    update_data = {
        "name": "Updated Product",
        "description": "Updated description",
        "price": 15.99,
        "quantity": 10,
    }

    update_response = client.put(
        f"/products/{product_id}",
        data=update_data,
        files={"image": ("updated.png", new_file, "image/png")},
    )
    
    assert update_response.status_code == 200
    updated_product = update_response.json()
    
    # Verificar que los campos se actualizaron correctamente
    assert updated_product["name"] == "Updated Product"
    assert updated_product["description"] == "Updated description"
    assert updated_product["price"] == 15.99
    assert updated_product["quantity"] == 10
    # Verificar que se generó una nueva URL de imagen
    assert "image_url" in updated_product
    assert updated_product["image_url"] != original_image_url
    assert updated_product["image_url"].startswith("/static/images/")

    # Test 2: Actualización parcial (sin imagen)
    partial_update_data = {
        "name": "Partially Updated",
        "quantity": 20,
    }

    partial_update_response = client.put(
        f"/products/{product_id}",
        data=partial_update_data,
    )
    
    assert partial_update_response.status_code == 200
    partially_updated = partial_update_response.json()
    
    # Verificar que solo se actualizaron los campos especificados
    assert partially_updated["name"] == "Partially Updated"
    assert partially_updated["quantity"] == 20
    # Los demás campos deberían mantenerse iguales
    assert partially_updated["description"] == "Updated description"
    assert partially_updated["price"] == 15.99
    # La URL de la imagen debería mantenerse igual
    assert partially_updated["image_url"] == updated_product["image_url"]

    # Test 3: Producto no encontrado
    non_existent_id = 9999
    response = client.put(
        f"/products/{non_existent_id}",
        data={"name": "No existe"},
    )
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()

    # Test 4: Validación de datos incorrectos
    # Probar con precio negativo
    invalid_price_data = {"price": -10}
    response = client.put(f"/products/{product_id}", data=invalid_price_data)
    assert response.status_code in [400, 422], f"Expected 400/422 for negative price, got {response.status_code}"
    
    # Probar con cantidad negativa
    invalid_quantity_data = {"quantity": -5}
    response = client.put(f"/products/{product_id}", data=invalid_quantity_data)
    assert response.status_code in [400, 422], f"Expected 400/422 for negative quantity, got {response.status_code}"
