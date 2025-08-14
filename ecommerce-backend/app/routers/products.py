from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductRead

router = APIRouter()


@router.post("/", response_model=ProductRead)
def create_product(product_in: ProductCreate, db: Session = Depends(get_db)):
    existing = db.query(Product).filter(Product.slug == product_in.slug).first()
    if existing:
        raise HTTPException(status_code=400, detail="Slug already exists")
    product = Product(**product_in.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


@router.get("/", response_model=list[ProductRead])
def list_products(
    db: Session = Depends(get_db),
    category_id: Optional[int] = Query(None),
    in_stock: Optional[bool] = Query(None),
    q: Optional[str] = Query(None),
):
    query = db.query(Product)
    if category_id is not None:
        query = query.filter(Product.category_id == category_id)
    if in_stock is not None:
        query = query.filter(Product.in_stock == in_stock)
    if q:
        like = f"%{q}%"
        query = query.filter(Product.name.ilike(like))
    return query.order_by(Product.id.desc()).all()


@router.get("/{product_id}", response_model=ProductRead)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.put("/{product_id}", response_model=ProductRead)
def update_product(product_id: int, product_in: ProductCreate, db: Session = Depends(get_db)):
    product = db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    for key, value in product_in.model_dump().items():
        setattr(product, key, value)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()
    return {"ok": True}