from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from order_service.app.core.dependencies import get_current_user, get_db
from order_service.app.schemas.auth_schema import AuthenticatedUser
from order_service.app.schemas.order_schema import CreateOrderRequest, OrderResponse, OrderStatusUpdate
from order_service.app.services.order_service import OrderService

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(
    payload: CreateOrderRequest,
    db: Session = Depends(get_db),
    actor: AuthenticatedUser = Depends(get_current_user),
) -> OrderResponse:
    return OrderService.create_order_from_cart(db, payload, actor)


@router.get("", response_model=list[OrderResponse])
def get_orders(
    db: Session = Depends(get_db),
    actor: AuthenticatedUser = Depends(get_current_user),
) -> list[OrderResponse]:
    return OrderService.get_orders(db, actor)


@router.get("/{order_id}", response_model=OrderResponse)
def get_order_by_id(
    order_id: int,
    db: Session = Depends(get_db),
    actor: AuthenticatedUser = Depends(get_current_user),
) -> OrderResponse:
    return OrderService.get_order_by_id(db, order_id, actor)


@router.put("/{order_id}/status", response_model=OrderResponse)
def update_order_status(
    order_id: int,
    payload: OrderStatusUpdate,
    db: Session = Depends(get_db),
    actor: AuthenticatedUser = Depends(get_current_user),
) -> OrderResponse:
    return OrderService.update_order_status(db, order_id, payload, actor)

