from sqlalchemy.orm import Session

from app.schemas import OrderBase
from .models import Pizza, Order

def get_pizza(db: Session, pizza_id: int):
    return db.query(Pizza).filter(Pizza.id == pizza_id).first()

def get_pizzas(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Pizza).filter(Pizza.is_active == True).offset(skip).limit(limit).all()

def create_order(db: Session, order: OrderBase):
    db_order = Order(**order.dict())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order