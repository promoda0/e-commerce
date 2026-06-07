from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from payment_service.app.core.constants import PaymentMethod, PaymentStatus


class PaymentCreate(BaseModel):
    order_id: int = Field(..., gt=0)
    amount: float = Field(..., gt=0)
    currency: str = Field(default="INR", min_length=3, max_length=10)
    payment_method: PaymentMethod
    gateway_name: str = Field(default="MOCK", min_length=2, max_length=50)
    simulate_failure: bool = False


class PaymentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    order_id: int
    user_id: int
    transaction_id: str | None
    amount: float
    currency: str
    payment_method: PaymentMethod
    payment_status: PaymentStatus
    gateway_name: str
    created_at: datetime
    updated_at: datetime


class RefundRequest(BaseModel):
    payment_id: int = Field(..., gt=0)
    reason: str | None = Field(default=None, max_length=250)

