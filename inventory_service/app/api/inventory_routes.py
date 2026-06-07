from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from inventory_service.app.core.dependencies import get_current_user, get_db, get_inventory_manager
from inventory_service.app.schemas.auth_schema import AuthenticatedUser
from inventory_service.app.schemas.inventory_schema import (
    InventoryCreate,
    InventoryResponse,
    InventoryUpdate,
    StockReleaseRequest,
    StockReservationRequest,
)
from inventory_service.app.services.inventory_service import InventoryService

router = APIRouter(prefix="/inventory", tags=["Inventory"])


@router.post("", response_model=InventoryResponse, status_code=status.HTTP_201_CREATED)
def create_inventory(
    payload: InventoryCreate,
    db: Session = Depends(get_db),
    _: AuthenticatedUser = Depends(get_inventory_manager),
) -> InventoryResponse:
    return InventoryService.initialize_inventory(db, payload)


@router.get("/{product_id}", response_model=InventoryResponse)
def get_inventory(
    product_id: int,
    db: Session = Depends(get_db),
    _: AuthenticatedUser = Depends(get_current_user),
) -> InventoryResponse:
    return InventoryService.get_inventory(db, product_id)


@router.put("/{product_id}", response_model=InventoryResponse)
def update_inventory(
    product_id: int,
    payload: InventoryUpdate,
    db: Session = Depends(get_db),
    _: AuthenticatedUser = Depends(get_inventory_manager),
) -> InventoryResponse:
    return InventoryService.update_inventory(db, product_id, payload)


@router.post("/reserve", response_model=InventoryResponse)
def reserve_stock(
    payload: StockReservationRequest,
    db: Session = Depends(get_db),
    _: AuthenticatedUser = Depends(get_inventory_manager),
) -> InventoryResponse:
    return InventoryService.reserve_stock(db, payload)


@router.post("/release", response_model=InventoryResponse)
def release_stock(
    payload: StockReleaseRequest,
    db: Session = Depends(get_db),
    _: AuthenticatedUser = Depends(get_inventory_manager),
) -> InventoryResponse:
    return InventoryService.release_stock(db, payload)

