from pydantic import BaseModel


class CartItemBase(BaseModel):
    product_id: int
    quantity: int


class CartItemCreate(CartItemBase):
    pass


class CartItemRead(CartItemBase):
    id: int
    unit_price: float

    class Config:
        from_attributes = True


class CartRead(BaseModel):
    id: int
    items: list[CartItemRead] = []

    class Config:
        from_attributes = True