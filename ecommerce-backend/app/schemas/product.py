from pydantic import BaseModel


class CategoryBase(BaseModel):
    name: str
    slug: str
    description: str | None = None


class CategoryCreate(CategoryBase):
    pass


class CategoryRead(CategoryBase):
    id: int

    class Config:
        from_attributes = True


class ProductBase(BaseModel):
    name: str
    slug: str
    description: str | None = None
    price: float
    in_stock: bool = True
    category_id: int | None = None


class ProductCreate(ProductBase):
    pass


class ProductRead(ProductBase):
    id: int

    class Config:
        from_attributes = True