from fastapi.testclient import TestClient
from jose import jwt

from order_service.app.core.constants import OrderStatus, UserRole
from order_service.app.core.database import Base, SessionLocal, engine
from order_service.app.core.security import JWT_ALGORITHM, JWT_SECRET_KEY
from order_service.app.main import app
from order_service.app.models.cart import Cart, CartItem
from order_service.app.models.product import Product


def _token(user_id: int, role: str) -> str:
    payload = {"sub": str(user_id), "role": role}
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)


def run_smoke_test() -> None:
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    db.query(CartItem).delete()
    db.query(Cart).delete()
    db.query(Product).delete()
    db.commit()

    product = Product(
        name="Order Smoke Product",
        description="Order service smoke test",
        category="Testing",
        brand="QA",
        price=100.0,
        stock_quantity=10,
        seller_id=999,
        is_active=True,
    )
    db.add(product)
    db.commit()
    db.refresh(product)

    cart = Cart(user_id=1001)
    db.add(cart)
    db.commit()
    db.refresh(cart)

    cart_item = CartItem(cart_id=cart.id, product_id=product.id, quantity=2)
    db.add(cart_item)
    db.commit()
    db.close()

    client = TestClient(app)
    customer_headers = {"Authorization": f"Bearer {_token(1001, UserRole.CUSTOMER.value)}"}
    admin_headers = {"Authorization": f"Bearer {_token(5001, UserRole.ADMIN.value)}"}

    create_response = client.post("/orders", headers=customer_headers, json={})
    assert create_response.status_code == 201, create_response.text
    body = create_response.json()
    assert body["status"] == OrderStatus.PENDING_PAYMENT.value
    assert body["total_amount"] == 200.0
    order_id = body["id"]

    own_orders = client.get("/orders", headers=customer_headers)
    assert own_orders.status_code == 200, own_orders.text
    assert len(own_orders.json()) >= 1

    admin_orders = client.get("/orders", headers=admin_headers)
    assert admin_orders.status_code == 200, admin_orders.text
    assert len(admin_orders.json()) >= 1

    status_update = client.put(
        f"/orders/{order_id}/status",
        headers=admin_headers,
        json={"status": OrderStatus.PROCESSING.value},
    )
    assert status_update.status_code == 200, status_update.text
    assert status_update.json()["status"] == OrderStatus.PROCESSING.value

    print("Order service smoke test passed")


if __name__ == "__main__":
    run_smoke_test()
