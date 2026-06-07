from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ProductCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=120)
    description: str | None = Field(default=None, max_length=5000)
    category: str | None = Field(default=None, max_length=100)
    brand: str | None = Field(default=None, max_length=100)
    price: float = Field(..., gt=0)
    stock_quantity: int = Field(default=0, ge=0)
    image_url: str | None = Field(default=None, max_length=512)
    seller_id: int | None = Field(default=None, gt=0)


class ProductUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=120)
    description: str | None = Field(default=None, max_length=5000)
    category: str | None = Field(default=None, max_length=100)
    brand: str | None = Field(default=None, max_length=100)
    price: float | None = Field(default=None, gt=0)
    stock_quantity: int | None = Field(default=None, ge=0)
    image_url: str | None = Field(default=None, max_length=512)
    is_active: bool | None = None


class ProductResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None
    category: str | None
    brand: str | None
    price: float
    stock_quantity: int
    image_url: str | None
    seller_id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime


class ProductListResponse(BaseModel):
    items: list[ProductResponse]
    total: int
    page: int
    page_size: int

