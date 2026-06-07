from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from cart_service.app.core.dependencies import get_db
from cart_service.app.schemas.cart_schema import (
    AddItemRequest,
    CartResponse,
    RemoveItemRequest,
    UpdateQuantityRequest,
)
from cart_service.app.services.cart_service import CartService

router = APIRouter(prefix="/cart", tags=["Cart"])


@router.post("/add", response_model=CartResponse)
def add_item(payload: AddItemRequest, db: Session = Depends(get_db)) -> CartResponse:
    return CartService.add_item(db, payload)


@router.delete("/remove", response_model=CartResponse)
def remove_item(payload: RemoveItemRequest, db: Session = Depends(get_db)) -> CartResponse:
    return CartService.remove_item(db, payload)


@router.put("/update", response_model=CartResponse)
def update_quantity(payload: UpdateQuantityRequest, db: Session = Depends(get_db)) -> CartResponse:
    return CartService.update_quantity(db, payload)


@router.get("/{user_id}", response_model=CartResponse)
def get_cart(user_id: int, db: Session = Depends(get_db)) -> CartResponse:
    return CartService.get_cart(db, user_id)

