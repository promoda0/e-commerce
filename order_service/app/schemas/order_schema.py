from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from order_service.app.core.constants import OrderStatus


class CreateOrderRequest(BaseModel):
    # Reserved for future checkout options (address, coupon, etc.).
    notes: str | None = Field(default=None, max_length=250)


class OrderItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    product_id: int
    quantity: int
    unit_price: float
    total_price: float


class OrderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    total_amount: float
    status: OrderStatus
    created_at: datetime
    updated_at: datetime
    items: list[OrderItemResponse]


class OrderStatusUpdate(BaseModel):
    status: OrderStatus

