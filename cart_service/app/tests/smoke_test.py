from sqlalchemy import text

from cart_service.app.core.database import Base, SessionLocal, engine
from cart_service.app.schemas.cart_schema import AddItemRequest, RemoveItemRequest, UpdateQuantityRequest
from cart_service.app.services.cart_service import CartService


def prepare_product_catalog(product_id: int, stock: int) -> None:
    db = SessionLocal()
    try:
        db.execute(
            text(
                """
                CREATE TABLE IF NOT EXISTS product (
                    id INTEGER PRIMARY KEY,
                    stock INTEGER NOT NULL
                )
                """
            )
        )
        db.execute(
            text(
                "INSERT OR REPLACE INTO product (id, stock) VALUES (:id, :stock)"
            ),
            {"id": product_id, "stock": stock},
        )
        db.commit()
    finally:
        db.close()


def run_smoke_test() -> None:
    Base.metadata.create_all(bind=engine)

    user_id = 501
    product_id = 1101
    prepare_product_catalog(product_id=product_id, stock=10)

    db = SessionLocal()
    try:
        add_result = CartService.add_item(
            db,
            AddItemRequest(user_id=user_id, product_id=product_id, quantity=2),
        )
        assert add_result.total_items == 2

        update_result = CartService.update_quantity(
            db,
            UpdateQuantityRequest(user_id=user_id, product_id=product_id, quantity=4),
        )
        assert update_result.total_items == 4

        get_result = CartService.get_cart(db, user_id=user_id)
        assert get_result.total_items == 4

        remove_result = CartService.remove_item(
            db,
            RemoveItemRequest(user_id=user_id, product_id=product_id),
        )
        assert remove_result.total_items == 0

        final_result = CartService.get_cart(db, user_id=user_id)
        assert final_result.total_items == 0

        print("Cart smoke test passed")
    finally:
        db.close()


if __name__ == "__main__":
    run_smoke_test()
