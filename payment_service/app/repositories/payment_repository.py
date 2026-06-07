from sqlalchemy.orm import Session

from payment_service.app.models.payment import Payment


class PaymentRepository:
    @staticmethod
    def create_payment(
        db: Session,
        *,
        order_id: int,
        user_id: int,
        transaction_id: str | None,
        amount: float,
        currency: str,
        payment_method: str,
        payment_status: str,
        gateway_name: str,
    ) -> Payment:
        payment = Payment(
            order_id=order_id,
            user_id=user_id,
            transaction_id=transaction_id,
            amount=amount,
            currency=currency,
            payment_method=payment_method,
            payment_status=payment_status,
            gateway_name=gateway_name,
        )
        db.add(payment)
        db.flush()
        db.refresh(payment)
        return payment

    @staticmethod
    def get_payment_by_id(db: Session, payment_id: int) -> Payment | None:
        return db.query(Payment).filter(Payment.id == payment_id).first()

    @staticmethod
    def get_payment_by_order(db: Session, order_id: int) -> Payment | None:
        return db.query(Payment).filter(Payment.order_id == order_id).order_by(Payment.created_at.desc()).first()

    @staticmethod
    def update_payment_status(
        db: Session,
        payment: Payment,
        *,
        payment_status: str,
        transaction_id: str | None = None,
    ) -> Payment:
        payment.payment_status = payment_status
        if transaction_id is not None:
            payment.transaction_id = transaction_id
        db.flush()
        db.refresh(payment)
        return payment

    @staticmethod
    def create_refund(db: Session, payment: Payment, refund_transaction_id: str) -> Payment:
        payment.payment_status = "REFUNDED"
        payment.transaction_id = refund_transaction_id
        db.flush()
        db.refresh(payment)
        return payment

