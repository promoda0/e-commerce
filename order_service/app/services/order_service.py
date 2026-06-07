from typing import Any

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from order_service.app.core.constants import OrderStatus, UserRole
from order_service.app.models.order import Order
from order_service.app.repositories.cart_repository import CartRepository
from order_service.app.repositories.order_repository import OrderRepository
from order_service.app.repositories.product_repository import ProductRepository
from order_service.app.schemas.auth_schema import AuthenticatedUser
from order_service.app.schemas.order_schema import CreateOrderRequest, OrderResponse, OrderStatusUpdate


class OrderService:
    @staticmethod
    def create_order_from_cart(
        db: Session,
        _: CreateOrderRequest,
        actor: AuthenticatedUser,
    ) -> OrderResponse:
        if actor.role != UserRole.CUSTOMER:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only customers can create orders",
            )

        cart = CartRepository.get_cart_with_items_by_user(db, actor.user_id)
        if not cart:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart not found")

        cart_id = OrderService._as_int(cart, "id")
        cart_items = CartRepository.get_cart_items(db, cart_id)
        if not cart_items:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Empty cart")

        product_ids = [OrderService._as_int(item, "product_id") for item in cart_items]
        products = ProductRepository.get_products_by_ids(db, product_ids)
        products_map = {OrderService._as_int(product, "id"): product for product in products}

        total_amount = 0.0
        order_lines: list[dict[str, float | int]] = []

        for item in cart_items:
            item_product_id = OrderService._as_int(item, "product_id")
            product = products_map.get(item_product_id)
            if not product or not bool(getattr(product, "is_active", False)):
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Product not found: {item_product_id}",
                )

            requested_quantity = OrderService._as_int(item, "quantity")
            available_stock = OrderService._as_int(product, "stock_quantity")
            if requested_quantity <= 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid quantity for product {item_product_id}",
                )
            if requested_quantity > available_stock:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Insufficient stock for product {item_product_id}",
                )

            unit_price = OrderService._as_float(product, "price")
            line_total = unit_price * requested_quantity
            total_amount += line_total
            order_lines.append(
                {
                    "product_id": OrderService._as_int(product, "id"),
                    "quantity": requested_quantity,
                    "unit_price": unit_price,
                    "total_price": line_total,
                }
            )

        try:
            order = OrderRepository.create_order(
                db,
                user_id=actor.user_id,
                total_amount=round(total_amount, 2),
                status=OrderStatus.PENDING_PAYMENT.value,
            )
            order_id = OrderService._as_int(order, "id")

            for line in order_lines:
                OrderRepository.create_order_item(
                    db,
                    order_id=order_id,
                    product_id=int(line["product_id"]),
                    quantity=int(line["quantity"]),
                    unit_price=float(line["unit_price"]),
                    total_price=float(line["total_price"]),
                )

                product = products_map[int(line["product_id"])]
                new_stock = OrderService._as_int(product, "stock_quantity") - int(line["quantity"])
                ProductRepository.update_stock(db, product, new_stock)

            CartRepository.clear_cart_items(db, cart_id)
            db.commit()
            created_order = OrderRepository.get_order_by_id(db, order_id)
            if not created_order:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Order not found after create")
            return OrderResponse.model_validate(created_order)
        except Exception:
            db.rollback()
            raise

    @staticmethod
    def get_orders(db: Session, actor: AuthenticatedUser) -> list[OrderResponse]:
        if actor.role in {UserRole.ADMIN, UserRole.SUPPORT_ADMIN}:
            orders = OrderRepository.get_all_orders(db)
        else:
            orders = OrderRepository.get_orders_by_user(db, actor.user_id)
        return [OrderResponse.model_validate(order) for order in orders]

    @staticmethod
    def get_order_by_id(db: Session, order_id: int, actor: AuthenticatedUser) -> OrderResponse:
        order = OrderRepository.get_order_by_id(db, order_id)
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

        if actor.role not in {UserRole.ADMIN, UserRole.SUPPORT_ADMIN} and OrderService._as_int(order, "user_id") != actor.user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Unauthorized access to order",
            )

        return OrderResponse.model_validate(order)

    @staticmethod
    def update_order_status(
        db: Session,
        order_id: int,
        payload: OrderStatusUpdate,
        actor: AuthenticatedUser,
    ) -> OrderResponse:
        if actor.role not in {UserRole.ADMIN, UserRole.SUPPORT_ADMIN}:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admin access required",
            )

        order = OrderRepository.get_order_by_id(db, order_id)
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

        OrderService._validate_status_transition(order, payload.status)

        try:
            updated = OrderRepository.update_order_status(db, order, payload.status.value)
            db.commit()
            refreshed = OrderRepository.get_order_by_id(db, OrderService._as_int(updated, "id"))
            if not refreshed:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Order missing after update")
            return OrderResponse.model_validate(refreshed)
        except Exception:
            db.rollback()
            raise

    @staticmethod
    def _validate_status_transition(order: Order, requested_status: OrderStatus) -> None:
        current_status = OrderStatus(str(getattr(order, "status")))

        if current_status == requested_status:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Order is already in status {requested_status.value}",
            )

        terminal_statuses = {OrderStatus.CANCELLED, OrderStatus.REFUNDED}
        if current_status in terminal_statuses and requested_status not in terminal_statuses:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Cannot transition from {current_status.value} to {requested_status.value}",
            )

    @staticmethod
    def _as_int(instance: Any, field_name: str) -> int:
        return int(getattr(instance, field_name))

    @staticmethod
    def _as_float(instance: Any, field_name: str) -> float:
        return float(getattr(instance, field_name))
