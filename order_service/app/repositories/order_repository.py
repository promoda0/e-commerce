from sqlalchemy.orm import Session, joinedload

from order_service.app.models.order import Order, OrderItem


class OrderRepository:
    @staticmethod
    def create_order(db: Session, *, user_id: int, total_amount: float, status: str) -> Order:
        order = Order(user_id=user_id, total_amount=total_amount, status=status)
        db.add(order)
        db.flush()
        db.refresh(order)
        return order

    @staticmethod
    def create_order_item(
        db: Session,
        *,
        order_id: int,
        product_id: int,
        quantity: int,
        unit_price: float,
        total_price: float,
    ) -> OrderItem:
        order_item = OrderItem(
            order_id=order_id,
            product_id=product_id,
            quantity=quantity,
            unit_price=unit_price,
            total_price=total_price,
        )
        db.add(order_item)
        db.flush()
        db.refresh(order_item)
        return order_item

    @staticmethod
    def get_order_by_id(db: Session, order_id: int) -> Order | None:
        return (
            db.query(Order)
            .options(joinedload(Order.items))
            .filter(Order.id == order_id)
            .first()
        )

    @staticmethod
    def get_orders_by_user(db: Session, user_id: int) -> list[Order]:
        return (
            db.query(Order)
            .options(joinedload(Order.items))
            .filter(Order.user_id == user_id)
            .order_by(Order.created_at.desc())
            .all()
        )

    @staticmethod
    def get_all_orders(db: Session) -> list[Order]:
        return db.query(Order).options(joinedload(Order.items)).order_by(Order.created_at.desc()).all()

    @staticmethod
    def update_order_status(db: Session, order: Order, status: str) -> Order:
        order.status = status
        db.flush()
        db.refresh(order)
        return order

