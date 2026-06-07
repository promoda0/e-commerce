from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from payment_service.app.core.constants import OrderStatus, PaymentStatus, UserRole
from payment_service.app.integrations.payment_processor_factory import PaymentProcessorFactory
from payment_service.app.integrations.payment_processors.types import PaymentProcessorRequest
from payment_service.app.models.order import Order
from payment_service.app.models.payment import Payment
from payment_service.app.repositories.order_repository import OrderRepository
from payment_service.app.repositories.payment_repository import PaymentRepository
from payment_service.app.schemas.auth_schema import AuthenticatedUser
from payment_service.app.schemas.payment_schema import PaymentCreate, PaymentResponse, RefundRequest


class PaymentService:
    @staticmethod
    def initiate_payment(db: Session, payload: PaymentCreate, actor: AuthenticatedUser) -> PaymentResponse:
        PaymentService._validate_customer_role(actor)

        order = PaymentService._get_order_or_404(db, payload.order_id)
        order_id = int(order.id)
        order_total_amount = float(order.total_amount)

        PaymentService._validate_order_ownership(order, actor)
        PaymentService._validate_amount(payload.amount, order_total_amount)
        PaymentService._validate_duplicate_payment(db, order_id)

        processor = PaymentProcessorFactory.create(payload.gateway_name)

        try:
            payment = PaymentRepository.create_payment(
                db,
                order_id=order_id,
                user_id=actor.user_id,
                transaction_id=None,
                amount=payload.amount,
                currency=payload.currency,
                payment_method=payload.payment_method.value,
                payment_status=PaymentStatus.PENDING.value,
                gateway_name=payload.gateway_name.upper(),
            )

            result = processor.process_payment(
                PaymentProcessorRequest(
                    order_id=order_id,
                    user_id=actor.user_id,
                    amount=payload.amount,
                    currency=payload.currency,
                    payment_method=payload.payment_method.value,
                    simulate_failure=payload.simulate_failure,
                )
            )

            if result.success:
                payment = PaymentRepository.update_payment_status(
                    db,
                    payment,
                    payment_status=PaymentStatus.SUCCESS.value,
                    transaction_id=result.transaction_id,
                )
                OrderRepository.update_order_status(db, order, OrderStatus.PAID.value)
            else:
                payment = PaymentRepository.update_payment_status(
                    db,
                    payment,
                    payment_status=PaymentStatus.FAILED.value,
                    transaction_id=result.transaction_id,
                )
                OrderRepository.update_order_status(db, order, OrderStatus.PENDING.value)

            db.commit()
            db.refresh(payment)
            return PaymentResponse.model_validate(payment)
        except Exception:
            db.rollback()
            raise

    @staticmethod
    def get_payment_by_id(db: Session, payment_id: int, actor: AuthenticatedUser) -> PaymentResponse:
        payment = PaymentRepository.get_payment_by_id(db, payment_id)
        if not payment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment not found")

        PaymentService._validate_view_permission(payment, actor)
        return PaymentResponse.model_validate(payment)

    @staticmethod
    def get_payment_by_order(db: Session, order_id: int, actor: AuthenticatedUser) -> PaymentResponse:
        payment = PaymentRepository.get_payment_by_order(db, order_id)
        if not payment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment not found for order")

        PaymentService._validate_view_permission(payment, actor)
        return PaymentResponse.model_validate(payment)

    @staticmethod
    def create_refund(db: Session, payload: RefundRequest, actor: AuthenticatedUser) -> PaymentResponse:
        payment = PaymentRepository.get_payment_by_id(db, payload.payment_id)
        if not payment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment not found")

        PaymentService._validate_view_permission(payment, actor)
        PaymentService._validate_refundable(payment)

        payment_order_id = int(payment.order_id)
        payment_gateway = str(payment.gateway_name)
        payment_transaction_id = str(payment.transaction_id or "")
        payment_amount = float(payment.amount)

        order = PaymentService._get_order_or_404(db, payment_order_id)

        processor = PaymentProcessorFactory.create(payment_gateway)
        refund_result = processor.process_refund(payment_transaction_id, payment_amount)
        if not refund_result.success:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Refund failed")

        try:
            refunded = PaymentRepository.create_refund(db, payment, refund_result.transaction_id)
            OrderRepository.update_order_status(db, order, OrderStatus.REFUNDED.value)
            db.commit()
            db.refresh(refunded)
            return PaymentResponse.model_validate(refunded)
        except Exception:
            db.rollback()
            raise

    @staticmethod
    def _get_order_or_404(db: Session, order_id: int) -> Order:
        order = OrderRepository.get_order_by_id(db, order_id)
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid order")
        return order

    @staticmethod
    def _validate_customer_role(actor: AuthenticatedUser) -> None:
        if actor.role != UserRole.CUSTOMER:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only customers can initiate payments",
            )

    @staticmethod
    def _validate_order_ownership(order: Order, actor: AuthenticatedUser) -> None:
        if order.user_id != actor.user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Unauthorized access to this order",
            )

    @staticmethod
    def _validate_amount(requested_amount: float, order_amount: float) -> None:
        if round(requested_amount, 2) != round(order_amount, 2):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Amount mismatch with order amount",
            )

    @staticmethod
    def _validate_duplicate_payment(db: Session, order_id: int) -> None:
        existing_payment = PaymentRepository.get_payment_by_order(db, order_id)
        if not existing_payment:
            return

        if existing_payment.payment_status in {PaymentStatus.PENDING.value, PaymentStatus.SUCCESS.value}:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Duplicate payment attempt for this order",
            )

    @staticmethod
    def _validate_view_permission(payment: Payment, actor: AuthenticatedUser) -> None:
        if payment.user_id == actor.user_id:
            return
        if actor.role in {UserRole.ADMIN, UserRole.SUPPORT_ADMIN}:
            return
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Unauthorized access to payment details",
        )

    @staticmethod
    def _validate_refundable(payment: Payment) -> None:
        if payment.payment_status == PaymentStatus.REFUNDED.value:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Payment is already refunded",
            )
        if payment.payment_status != PaymentStatus.SUCCESS.value:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Only successful payments can be refunded",
            )
