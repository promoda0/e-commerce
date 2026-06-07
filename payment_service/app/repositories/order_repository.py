from sqlalchemy.orm import Session

from payment_service.app.models.order import Order


class OrderRepository:
    @staticmethod
    def get_order_by_id(db: Session, order_id: int) -> Order | None:
        return db.query(Order).filter(Order.id == order_id).first()

    @staticmethod
    def update_order_status(db: Session, order: Order, status: str) -> Order:
        order.status = status
        db.flush()
        db.refresh(order)
        return order

