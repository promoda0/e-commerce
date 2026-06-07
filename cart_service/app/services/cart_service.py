from typing import cast

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from cart_service.app.models.cart import Cart, CartItem
from cart_service.app.repositories.cart_repository import CartRepository
from cart_service.app.repositories.product_repository import ProductRepository
from cart_service.app.schemas.cart_schema import (
    AddItemRequest,
    CartItemResponse,
    CartResponse,
    RemoveItemRequest,
    UpdateQuantityRequest,
)


class CartService:
    """Service layer contains cart business rules and validations."""

    @staticmethod
    def add_item(db: Session, payload: AddItemRequest) -> CartResponse:
        CartService._validate_quantity(payload.quantity)

        stock = ProductRepository.get_stock_by_product_id(db, payload.product_id)
        if stock is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found in catalog",
            )

        existing_item = CartRepository.get_cart_item(db, payload.user_id, payload.product_id)
        existing_quantity = existing_item.quantity if existing_item else 0

        if existing_quantity + payload.quantity > stock:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Requested quantity exceeds available stock",
            )

        cart = CartRepository.add_item(
            db=db,
            user_id=payload.user_id,
            product_id=payload.product_id,
            quantity=payload.quantity,
        )
        return CartService._to_cart_response(cart)

    @staticmethod
    def remove_item(db: Session, payload: RemoveItemRequest) -> CartResponse:
        cart = CartRepository.remove_item(
            db=db,
            user_id=payload.user_id,
            product_id=payload.product_id,
        )
        if cart is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cart item not found",
            )
        return CartService._to_cart_response(cart)

    @staticmethod
    def update_quantity(db: Session, payload: UpdateQuantityRequest) -> CartResponse:
        CartService._validate_quantity(payload.quantity)

        stock = ProductRepository.get_stock_by_product_id(db, payload.product_id)
        if stock is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found in catalog",
            )

        if payload.quantity > stock:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Requested quantity exceeds available stock",
            )

        cart = CartRepository.update_quantity(
            db=db,
            user_id=payload.user_id,
            product_id=payload.product_id,
            quantity=payload.quantity,
        )
        if cart is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cart item not found",
            )
        return CartService._to_cart_response(cart)

    @staticmethod
    def get_cart(db: Session, user_id: int) -> CartResponse:
        cart = CartRepository.get_cart(db, user_id)
        if cart is None:
            return CartResponse(user_id=user_id, total_items=0, items=[])
        return CartService._to_cart_response(cart)

    @staticmethod
    def _validate_quantity(quantity: int) -> None:
        if quantity <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Quantity must be greater than zero",
            )

    @staticmethod
    def _to_cart_response(cart: Cart) -> CartResponse:
        cart_items = cast(list[CartItem], cart.items)
        items = [
            CartItemResponse(product_id=item.product_id, quantity=item.quantity)
            for item in sorted(cart_items, key=lambda cart_item: cart_item.product_id)
        ]
        total_items = sum(item.quantity for item in items)
        return CartResponse(user_id=int(cart.user_id), total_items=total_items, items=items)
