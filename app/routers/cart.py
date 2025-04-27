from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..auth import get_current_user
from ..database import get_db
from ..models import Cart, Pizza, User
from ..schemas import CartItem, CartCreate, CartResponse

router = APIRouter(prefix="/cart", tags=["cart"])

@router.get("/", response_model=CartResponse)
def get_cart(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
    if not cart:
        cart = Cart(user_id=current_user.id, items=[])
        db.add(cart)
        db.commit()
        db.refresh(cart)

    total = 0
    for item in cart.items:
        pizza = db.query(Pizza).filter(Pizza.id == item["pizza_id"]).first()
        if pizza:
            total += pizza.price * item["quantity"]

    return {"id": cart.id, "items": cart.items, "total": total}


@router.post("/add", response_model=CartResponse)
def add_to_cart(
        item: CartItem,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
    if not cart:
        cart = Cart(user_id=current_user.id, items=[])
        db.add(cart)

    # Проверяем есть ли пицца
    pizza = db.query(Pizza).filter(Pizza.id == item.pizza_id).first()
    if not pizza:
        raise HTTPException(status_code=404, detail="Pizza not found")

    # Обновляем корзину
    items = cart.items.copy()
    found = False
    for i in items:
        if i["pizza_id"] == item.pizza_id:
            i["quantity"] += item.quantity
            found = True
            break

    if not found:
        items.append({"pizza_id": item.pizza_id, "quantity": item.quantity})

    cart.items = items
    db.commit()
    db.refresh(cart)

    return get_cart(db, current_user)


@router.post("/remove", response_model=CartResponse)
def remove_from_cart(
        pizza_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")

    items = [item for item in cart.items if item["pizza_id"] != pizza_id]
    cart.items = items
    db.commit()
    db.refresh(cart)

    return get_cart(db, current_user)


@router.delete("/clear", response_model=CartResponse)
def clear_cart(
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")

    cart.items = []
    db.commit()
    db.refresh(cart)

    return {"id": cart.id, "items": [], "total": 0}