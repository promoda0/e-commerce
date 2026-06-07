from fastapi.testclient import TestClient
from jose import jwt

from inventory_service.app.core.constants import StockReleaseMode, UserRole
from inventory_service.app.core.database import Base, SessionLocal, engine
from inventory_service.app.core.security import JWT_ALGORITHM, JWT_SECRET_KEY
from inventory_service.app.main import app
from inventory_service.app.models.inventory import Inventory
from inventory_service.app.models.product import Product


def _token(user_id: int, role: str) -> str:
    payload = {"sub": str(user_id), "role": role}
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)


def run_smoke_test() -> None:
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    db.query(Inventory).delete()
    db.query(Product).delete()
    db.commit()

    product = Product(
        name="Inventory Smoke Product",
        description="Inventory service smoke test",
        category="Testing",
        brand="QA",
        price=200.0,
        stock_quantity=50,
        seller_id=901,
        is_active=True,
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    product_id = product.id
    db.close()

    manager_headers = {"Authorization": f"Bearer {_token(3001, UserRole.ADMIN.value)}"}
    reader_headers = {"Authorization": f"Bearer {_token(4001, UserRole.CUSTOMER.value)}"}

    client = TestClient(app)

    create_response = client.post(
        "/inventory",
        headers=manager_headers,
        json={"product_id": product_id, "total_stock": 20, "reserved_stock": 0, "reorder_level": 5},
    )
    assert create_response.status_code == 201, create_response.text

    reserve_response = client.post(
        "/inventory/reserve",
        headers=manager_headers,
        json={"product_id": product_id, "quantity": 4},
    )
    assert reserve_response.status_code == 200, reserve_response.text
    assert reserve_response.json()["reserved_stock"] == 4

    deduct_response = client.post(
        "/inventory/release",
        headers=manager_headers,
        json={"product_id": product_id, "quantity": 3, "mode": StockReleaseMode.DEDUCT.value},
    )
    assert deduct_response.status_code == 200, deduct_response.text
    assert deduct_response.json()["total_stock"] == 17
    assert deduct_response.json()["reserved_stock"] == 1

    read_response = client.get(f"/inventory/{product_id}", headers=reader_headers)
    assert read_response.status_code == 200, read_response.text

    print("Inventory service smoke test passed")


if __name__ == "__main__":
    run_smoke_test()

