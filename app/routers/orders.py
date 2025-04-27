from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import Order, Pizza
from app.schemas import OrderCreate, OrderResponse

router = APIRouter(
    prefix="/orders",
    tags=["orders"]
)


@router.post("/", response_model=OrderResponse)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    # Проверяем существует ли пицца
    db_pizza = db.query(Pizza).filter(Pizza.id == order.pizza_id).first()
    if not db_pizza:
        raise HTTPException(status_code=404, detail="Pizza not found")

    # Создаем заказ
    db_order = Order(
        pizza_id=order.pizza_id,
        customer_name=order.customer_name,
        address=order.address,
        status="pending"
    )

    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


@router.get("/", response_model=List[OrderResponse])
def read_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    orders = db.query(Order).offset(skip).limit(limit).all()
    return orders


@router.get("/{order_id}", response_model=OrderResponse)
def read_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.put("/{order_id}", response_model=OrderResponse)
def update_order_status(order_id: int, status: str, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")

    order.status = status
    db.commit()
    db.refresh(order)
    return order