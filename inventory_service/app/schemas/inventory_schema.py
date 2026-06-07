from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from inventory_service.app.core.constants import StockReleaseMode


class InventoryCreate(BaseModel):
    product_id: int = Field(..., gt=0)
    total_stock: int = Field(..., ge=0)
    reserved_stock: int = Field(default=0, ge=0)
    reorder_level: int = Field(default=0, ge=0)


class InventoryUpdate(BaseModel):
    stock_delta: int | None = None
    reorder_level: int | None = Field(default=None, ge=0)


class InventoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    product_id: int
    total_stock: int
    reserved_stock: int
    available_stock: int
    reorder_level: int
    is_low_stock: bool
    created_at: datetime
    updated_at: datetime


class StockReservationRequest(BaseModel):
    product_id: int = Field(..., gt=0)
    quantity: int = Field(..., gt=0)


class StockReleaseRequest(BaseModel):
    product_id: int = Field(..., gt=0)
    quantity: int = Field(..., gt=0)
    mode: StockReleaseMode = StockReleaseMode.RELEASE

