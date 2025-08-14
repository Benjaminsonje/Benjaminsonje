from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.db.session import get_db
from app.models.category import Category
from app.schemas.product import CategoryCreate, CategoryRead

router = APIRouter()


@router.post("/", response_model=CategoryRead)
def create_category(category_in: CategoryCreate, db: Session = Depends(get_db)):
    existing_slug = db.query(Category).filter(Category.slug == category_in.slug).first()
    if existing_slug:
        raise HTTPException(status_code=400, detail="Slug already exists")
    existing_name = db.query(Category).filter(Category.name == category_in.name).first()
    if existing_name:
        raise HTTPException(status_code=400, detail="Name already exists")
    category = Category(**category_in.model_dump())
    db.add(category)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Category already exists")
    db.refresh(category)
    return category


@router.get("/", response_model=list[CategoryRead])
def list_categories(db: Session = Depends(get_db)):
    return db.query(Category).order_by(Category.name.asc()).all()


@router.get("/{category_id}", response_model=CategoryRead)
def get_category(category_id: int, db: Session = Depends(get_db)):
    category = db.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.put("/{category_id}", response_model=CategoryRead)
def update_category(category_id: int, category_in: CategoryCreate, db: Session = Depends(get_db)):
    category = db.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    # Ensure slug/name uniqueness when updating
    conflict_slug = (
        db.query(Category)
        .filter(Category.slug == category_in.slug, Category.id != category_id)
        .first()
    )
    if conflict_slug:
        raise HTTPException(status_code=400, detail="Slug already exists")
    conflict_name = (
        db.query(Category)
        .filter(Category.name == category_in.name, Category.id != category_id)
        .first()
    )
    if conflict_name:
        raise HTTPException(status_code=400, detail="Name already exists")

    for key, value in category_in.model_dump().items():
        setattr(category, key, value)
    db.add(category)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Category already exists")
    db.refresh(category)
    return category


@router.delete("/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db)):
    category = db.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(category)
    db.commit()
    return {"ok": True}