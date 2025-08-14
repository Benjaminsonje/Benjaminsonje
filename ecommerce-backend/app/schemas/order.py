from datetime import datetime
from pydantic import BaseModel


class OrderItemBase(BaseModel):
    product_id: int | None = None
    quantity: int
    unit_price: float


class OrderItemCreate(OrderItemBase):
    pass


class OrderItemRead(OrderItemBase):
    id: int

    class Config:
        from_attributes = True


class OrderBase(BaseModel):
    status: str = "pending"


class OrderCreate(OrderBase):
    address_id: int | None = None


class OrderRead(OrderBase):
    id: int
    user_id: int | None = None
    total_amount: float
    created_at: datetime
    items: list[OrderItemRead] = []

    class Config:
        from_attributes = True