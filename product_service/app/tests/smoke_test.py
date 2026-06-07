from fastapi.testclient import TestClient
from jose import jwt

from product_service.app.core.constants import UserRole
from product_service.app.core.database import Base, SessionLocal, engine
from product_service.app.core.security import JWT_ALGORITHM, JWT_SECRET_KEY
from product_service.app.main import app
from product_service.app.models.product import Product


def _make_token(user_id: int, role: str) -> str:
    payload = {"sub": str(user_id), "role": role}
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)


def run_smoke_test() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    db.query(Product).delete()
    db.commit()
    db.close()

    client = TestClient(app)

    seller_headers = {"Authorization": f"Bearer {_make_token(1001, UserRole.SELLER.value)}"}
    customer_headers = {"Authorization": f"Bearer {_make_token(2001, UserRole.CUSTOMER.value)}"}

    create_payload = {
        "name": "Smoke Test Product",
        "description": "Used by automated smoke test",
        "category": "Testing",
        "brand": "QA",
        "price": 120.0,
        "stock_quantity": 5,
        "image_url": "https://example.com/image.png",
    }

    create_response = client.post("/products", json=create_payload, headers=seller_headers)
    assert create_response.status_code == 201, create_response.text
    created = create_response.json()
    product_id = created["id"]

    list_response = client.get("/products", headers=customer_headers)
    assert list_response.status_code == 200, list_response.text
    assert list_response.json()["total"] >= 1

    search_response = client.get("/products/search", params={"name": "Smoke"}, headers=customer_headers)
    assert search_response.status_code == 200, search_response.text
    assert search_response.json()["total"] >= 1

    update_response = client.put(
        f"/products/{product_id}",
        json={"price": 140.0, "stock_quantity": 7},
        headers=seller_headers,
    )
    assert update_response.status_code == 200, update_response.text
    assert update_response.json()["price"] == 140.0

    delete_response = client.delete(f"/products/{product_id}", headers=seller_headers)
    assert delete_response.status_code == 204, delete_response.text

    print("Product service smoke test passed")


if __name__ == "__main__":
    run_smoke_test()
