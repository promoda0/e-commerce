from pydantic import BaseModel, Field


class AddItemRequest(BaseModel):
    user_id: int = Field(..., gt=0)
    product_id: int = Field(..., gt=0)
    quantity: int = Field(..., gt=0)


class RemoveItemRequest(BaseModel):
    user_id: int = Field(..., gt=0)
    product_id: int = Field(..., gt=0)


class UpdateQuantityRequest(BaseModel):
    user_id: int = Field(..., gt=0)
    product_id: int = Field(..., gt=0)
    quantity: int = Field(..., gt=0)


class CartItemResponse(BaseModel):
    product_id: int
    quantity: int


class CartResponse(BaseModel):
    user_id: int
    total_items: int
    items: list[CartItemResponse]

