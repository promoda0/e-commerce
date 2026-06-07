from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from payment_service.app.core.dependencies import get_current_user, get_db
from payment_service.app.schemas.auth_schema import AuthenticatedUser
from payment_service.app.schemas.payment_schema import PaymentCreate, PaymentResponse, RefundRequest
from payment_service.app.services.payment_service import PaymentService

router = APIRouter(prefix="/payments", tags=["Payments"])


@router.post("/initiate", response_model=PaymentResponse, status_code=status.HTTP_201_CREATED)
def initiate_payment(
    payload: PaymentCreate,
    db: Session = Depends(get_db),
    actor: AuthenticatedUser = Depends(get_current_user),
) -> PaymentResponse:
    return PaymentService.initiate_payment(db, payload, actor)


@router.get("/{payment_id}", response_model=PaymentResponse)
def get_payment_by_id(
    payment_id: int,
    db: Session = Depends(get_db),
    actor: AuthenticatedUser = Depends(get_current_user),
) -> PaymentResponse:
    return PaymentService.get_payment_by_id(db, payment_id, actor)


@router.get("/order/{order_id}", response_model=PaymentResponse)
def get_payment_by_order(
    order_id: int,
    db: Session = Depends(get_db),
    actor: AuthenticatedUser = Depends(get_current_user),
) -> PaymentResponse:
    return PaymentService.get_payment_by_order(db, order_id, actor)


@router.post("/refund", response_model=PaymentResponse)
def create_refund(
    payload: RefundRequest,
    db: Session = Depends(get_db),
    actor: AuthenticatedUser = Depends(get_current_user),
) -> PaymentResponse:
    return PaymentService.create_refund(db, payload, actor)

