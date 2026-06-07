from datetime import datetime
from typing import Any

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from inventory_service.app.core.constants import StockReleaseMode
from inventory_service.app.models.inventory import Inventory
from inventory_service.app.repositories.inventory_repository import InventoryRepository
from inventory_service.app.repositories.product_repository import ProductRepository
from inventory_service.app.schemas.inventory_schema import (
    InventoryCreate,
    InventoryResponse,
    InventoryUpdate,
    StockReleaseRequest,
    StockReservationRequest,
)


class InventoryService:
    @staticmethod
    def initialize_inventory(db: Session, payload: InventoryCreate) -> InventoryResponse:
        product = ProductRepository.get_by_id(db, payload.product_id)
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

        existing = InventoryRepository.get_inventory_by_product(db, payload.product_id)
        if existing:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Inventory already exists for product")

        if payload.reserved_stock > payload.total_stock:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Reserved stock cannot exceed total stock",
            )

        available_stock = payload.total_stock - payload.reserved_stock

        try:
            inventory = InventoryRepository.create_inventory(
                db,
                product_id=payload.product_id,
                total_stock=payload.total_stock,
                reserved_stock=payload.reserved_stock,
                available_stock=available_stock,
                reorder_level=payload.reorder_level,
            )
            db.commit()
            return InventoryService._to_response(inventory)
        except Exception:
            db.rollback()
            raise

    @staticmethod
    def get_inventory(db: Session, product_id: int) -> InventoryResponse:
        inventory = InventoryRepository.get_inventory_by_product(db, product_id)
        if not inventory:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product inventory not found")
        return InventoryService._to_response(inventory)

    @staticmethod
    def update_inventory(db: Session, product_id: int, payload: InventoryUpdate) -> InventoryResponse:
        inventory = InventoryService._get_inventory_or_404(db, product_id)

        if payload.stock_delta is None and payload.reorder_level is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Provide stock_delta and/or reorder_level",
            )

        current_total = InventoryService._as_int(inventory, "total_stock")
        current_reserved = InventoryService._as_int(inventory, "reserved_stock")
        current_reorder = InventoryService._as_int(inventory, "reorder_level")

        new_total = current_total + int(payload.stock_delta or 0)
        new_reorder = int(payload.reorder_level if payload.reorder_level is not None else current_reorder)

        if new_total < 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid stock update")
        if current_reserved > new_total:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Reserved stock cannot exceed total stock",
            )

        new_available = new_total - current_reserved

        try:
            updated = InventoryRepository.update_stock(
                db,
                inventory,
                total_stock=new_total,
                available_stock=new_available,
                reorder_level=new_reorder,
            )
            db.commit()
            return InventoryService._to_response(updated)
        except Exception:
            db.rollback()
            raise

    @staticmethod
    def reserve_stock(db: Session, payload: StockReservationRequest) -> InventoryResponse:
        inventory = InventoryService._get_inventory_or_404(db, payload.product_id)

        if InventoryService._as_int(inventory, "available_stock") < payload.quantity:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Insufficient stock")

        try:
            reserved = InventoryRepository.reserve_stock(db, inventory, payload.quantity)
            db.commit()
            return InventoryService._to_response(reserved)
        except Exception:
            db.rollback()
            raise

    @staticmethod
    def release_stock(db: Session, payload: StockReleaseRequest) -> InventoryResponse:
        inventory = InventoryService._get_inventory_or_404(db, payload.product_id)

        if payload.quantity > InventoryService._as_int(inventory, "reserved_stock"):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid reservation release")

        deduct = payload.mode == StockReleaseMode.DEDUCT
        try:
            released = InventoryRepository.release_stock(db, inventory, payload.quantity, deduct=deduct)
            db.commit()
            return InventoryService._to_response(released)
        except Exception:
            db.rollback()
            raise

    @staticmethod
    def _get_inventory_or_404(db: Session, product_id: int) -> Inventory:
        inventory = InventoryRepository.get_inventory_by_product(db, product_id)
        if not inventory:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product inventory not found")
        return inventory

    @staticmethod
    def check_low_stock(inventory: Inventory) -> bool:
        return InventoryService._as_int(inventory, "available_stock") <= InventoryService._as_int(inventory, "reorder_level")

    @staticmethod
    def _to_response(inventory: Inventory) -> InventoryResponse:
        return InventoryResponse(
            id=InventoryService._as_int(inventory, "id"),
            product_id=InventoryService._as_int(inventory, "product_id"),
            total_stock=InventoryService._as_int(inventory, "total_stock"),
            reserved_stock=InventoryService._as_int(inventory, "reserved_stock"),
            available_stock=InventoryService._as_int(inventory, "available_stock"),
            reorder_level=InventoryService._as_int(inventory, "reorder_level"),
            is_low_stock=InventoryService.check_low_stock(inventory),
            created_at=InventoryService._as_datetime(inventory, "created_at"),
            updated_at=InventoryService._as_datetime(inventory, "updated_at"),
        )

    @staticmethod
    def _as_int(instance: Any, field_name: str) -> int:
        return int(getattr(instance, field_name))

    @staticmethod
    def _as_datetime(instance: Any, field_name: str) -> datetime:
        value = getattr(instance, field_name)
        if not isinstance(value, datetime):
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Invalid datetime in inventory")
        return value
