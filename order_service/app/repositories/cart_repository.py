from sqlalchemy.orm import Session

from order_service.app.models.cart import Cart, CartItem


class CartRepository:
    @staticmethod
    def get_cart_with_items_by_user(db: Session, user_id: int) -> Cart | None:
        return db.query(Cart).filter(Cart.user_id == user_id).first()

    @staticmethod
    def get_cart_items(db: Session, cart_id: int) -> list[CartItem]:
        return db.query(CartItem).filter(CartItem.cart_id == cart_id).all()

    @staticmethod
    def clear_cart_items(db: Session, cart_id: int) -> None:
        db.query(CartItem).filter(CartItem.cart_id == cart_id).delete(synchronize_session=False)

