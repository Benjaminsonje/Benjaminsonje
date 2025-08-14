from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.deps import get_current_active_user
from app.db.session import get_db
from app.models.cart import Cart, CartItem
from app.models.product import Product
from app.models.user import User
from app.schemas.cart import CartItemCreate, CartRead, CartItemRead

router = APIRouter()


def _get_or_create_cart(db: Session, user_id: int) -> Cart:
    cart = db.query(Cart).filter(Cart.user_id == user_id).first()
    if not cart:
        cart = Cart(user_id=user_id)
        db.add(cart)
        db.commit()
        db.refresh(cart)
    return cart


@router.get("/me", response_model=CartRead)
def get_my_cart(db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    cart = _get_or_create_cart(db, current_user.id)
    items = db.query(CartItem).filter(CartItem.cart_id == cart.id).all()
    return {"id": cart.id, "items": items}


@router.post("/me/items", response_model=CartRead)
def add_item_to_my_cart(
    item_in: CartItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    cart = _get_or_create_cart(db, current_user.id)
    product = db.get(Product, item_in.product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    cart_item = db.query(CartItem).filter(
        CartItem.cart_id == cart.id, CartItem.product_id == item_in.product_id
    ).first()
    if cart_item:
        cart_item.quantity += item_in.quantity
    else:
        cart_item = CartItem(
            cart_id=cart.id,
            product_id=item_in.product_id,
            quantity=item_in.quantity,
            unit_price=product.price,
        )
        db.add(cart_item)
    db.commit()
    items = db.query(CartItem).filter(CartItem.cart_id == cart.id).all()
    return {"id": cart.id, "items": items}


@router.delete("/me/items/{item_id}", response_model=CartRead)
def remove_item_from_my_cart(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    cart = _get_or_create_cart(db, current_user.id)
    cart_item = db.get(CartItem, item_id)
    if not cart_item or cart_item.cart_id != cart.id:
        raise HTTPException(status_code=404, detail="Item not found in cart")
    db.delete(cart_item)
    db.commit()
    items = db.query(CartItem).filter(CartItem.cart_id == cart.id).all()
    return {"id": cart.id, "items": items}