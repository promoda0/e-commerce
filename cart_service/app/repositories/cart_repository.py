from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from cart_service.app.models.cart import Cart, CartItem


class CartRepository:
    """Repository handles only persistence logic for carts and cart items."""

    @staticmethod
    def get_cart(db: Session, user_id: int) -> Cart | None:
        stmt = (
            select(Cart)
            .options(joinedload(Cart.items))
            .where(Cart.user_id == user_id)
        )
        return db.execute(stmt).scalars().first()

    @staticmethod
    def get_or_create_cart(db: Session, user_id: int) -> Cart:
        cart = CartRepository.get_cart(db, user_id)
        if cart:
            return cart

        cart = Cart(user_id=user_id)
        db.add(cart)
        db.commit()
        db.refresh(cart)
        return cart

    @staticmethod
    def get_cart_item(db: Session, user_id: int, product_id: int) -> CartItem | None:
        cart = CartRepository.get_cart(db, user_id)
        if not cart:
            return None

        stmt = select(CartItem).where(
            CartItem.cart_id == cart.id,
            CartItem.product_id == product_id,
        )
        return db.execute(stmt).scalars().first()

    @staticmethod
    def add_item(db: Session, user_id: int, product_id: int, quantity: int) -> Cart:
        cart = CartRepository.get_or_create_cart(db, user_id)
        item = db.execute(
            select(CartItem).where(
                CartItem.cart_id == cart.id,
                CartItem.product_id == product_id,
            )
        ).scalars().first()

        if item:
            item.quantity += quantity
        else:
            item = CartItem(cart_id=cart.id, product_id=product_id, quantity=quantity)
            db.add(item)

        db.commit()
        return CartRepository.get_cart(db, user_id)

    @staticmethod
    def remove_item(db: Session, user_id: int, product_id: int) -> Cart | None:
        cart = CartRepository.get_cart(db, user_id)
        if not cart:
            return None

        item = db.execute(
            select(CartItem).where(
                CartItem.cart_id == cart.id,
                CartItem.product_id == product_id,
            )
        ).scalars().first()

        if not item:
            return None

        db.delete(item)
        db.commit()
        return CartRepository.get_cart(db, user_id)

    @staticmethod
    def update_quantity(db: Session, user_id: int, product_id: int, quantity: int) -> Cart | None:
        cart = CartRepository.get_cart(db, user_id)
        if not cart:
            return None

        item = db.execute(
            select(CartItem).where(
                CartItem.cart_id == cart.id,
                CartItem.product_id == product_id,
            )
        ).scalars().first()

        if not item:
            return None

        item.quantity = quantity
        db.commit()
        return CartRepository.get_cart(db, user_id)

