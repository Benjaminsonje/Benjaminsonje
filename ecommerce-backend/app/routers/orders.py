from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.deps import get_current_active_user
from app.db.session import get_db
from app.models.cart import Cart, CartItem
from app.models.order import Order, OrderItem
from app.models.user import User
from app.schemas.order import OrderCreate, OrderRead

router = APIRouter()


def _get_cart(db: Session, user_id: int) -> Cart | None:
    return db.query(Cart).filter(Cart.user_id == user_id).first()


@router.post("/me", response_model=OrderRead)
def place_order(
    order_in: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    cart = _get_cart(db, current_user.id)
    if not cart:
        raise HTTPException(status_code=400, detail="Cart is empty")
    items = db.query(CartItem).filter(CartItem.cart_id == cart.id).all()
    if not items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    total = sum(float(item.unit_price) * item.quantity for item in items)
    order = Order(user_id=current_user.id, status="pending", total_amount=total)
    db.add(order)
    db.commit()
    db.refresh(order)

    for item in items:
        db.add(
            OrderItem(
                order_id=order.id,
                product_id=item.product_id,
                quantity=item.quantity,
                unit_price=item.unit_price,
            )
        )
    # Clear cart
    for item in items:
        db.delete(item)

    db.commit()

    # Reload with items for response if needed
    order_items = db.query(OrderItem).filter(OrderItem.order_id == order.id).all()
    return {
        "id": order.id,
        "status": order.status,
        "user_id": order.user_id,
        "total_amount": float(order.total_amount),
        "created_at": order.created_at,
        "items": order_items,
    }


@router.get("/me", response_model=list[OrderRead])
def list_my_orders(db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    orders = db.query(Order).filter(Order.user_id == current_user.id).order_by(Order.id.desc()).all()
    results: list[OrderRead] = []
    for order in orders:
        items = db.query(OrderItem).filter(OrderItem.order_id == order.id).all()
        results.append(
            OrderRead(
                id=order.id,
                user_id=order.user_id,
                total_amount=float(order.total_amount),
                created_at=order.created_at,
                status=order.status,
                items=items,
            )
        )
    return results