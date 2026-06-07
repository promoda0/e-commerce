from fastapi.testclient import TestClient
from jose import jwt

from payment_service.app.core.constants import OrderStatus, UserRole
from payment_service.app.core.database import Base, SessionLocal, engine
from payment_service.app.core.security import JWT_ALGORITHM, JWT_SECRET_KEY
from payment_service.app.main import create_app
from payment_service.app.models.order import Order
from payment_service.app.models.payment import Payment


def _token(user_id: int, role: str) -> str:
    payload = {"sub": str(user_id), "role": role}
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)


def run_smoke_test() -> None:
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    db.query(Payment).delete()
    db.query(Order).delete()

    order = Order(user_id=1001, total_amount=499.0, status=OrderStatus.PENDING.value)
    db.add(order)
    db.commit()
    db.refresh(order)
    order_id = order.id
    db.close()

    client = TestClient(create_app())
    customer_headers = {"Authorization": f"Bearer {_token(1001, UserRole.CUSTOMER.value)}"}

    initiate_response = client.post(
        "/payments/initiate",
        headers=customer_headers,
        json={
            "order_id": order_id,
            "amount": 499.0,
            "currency": "INR",
            "payment_method": "UPI",
            "gateway_name": "MOCK",
        },
    )
    assert initiate_response.status_code == 201, initiate_response.text
    payment_id = initiate_response.json()["id"]

    get_response = client.get(f"/payments/{payment_id}", headers=customer_headers)
    assert get_response.status_code == 200, get_response.text
    assert get_response.json()["payment_status"] == "SUCCESS"

    refund_response = client.post(
        "/payments/refund",
        headers=customer_headers,
        json={"payment_id": payment_id, "reason": "Customer requested refund"},
    )
    assert refund_response.status_code == 200, refund_response.text
    assert refund_response.json()["payment_status"] == "REFUNDED"

    print("Payment service smoke test passed")


if __name__ == "__main__":
    run_smoke_test()
