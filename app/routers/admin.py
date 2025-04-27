from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import Pizza
from app.schemas import PizzaCreate, PizzaResponse

router = APIRouter(
    prefix="/admin",
    tags=["admin"]
)


@router.post("/pizzas/", response_model=PizzaResponse)
def create_pizza(pizza: PizzaCreate, db: Session = Depends(get_db)):
    db_pizza = Pizza(
        name=pizza.name,
        description=pizza.description,
        price=pizza.price
    )
    db.add(db_pizza)
    db.commit()
    db.refresh(db_pizza)
    return db_pizza


@router.put("/pizzas/{pizza_id}", response_model=PizzaResponse)
def update_pizza(pizza_id: int, pizza: PizzaCreate, db: Session = Depends(get_db)):
    db_pizza = db.query(Pizza).filter(Pizza.id == pizza_id).first()
    if not db_pizza:
        raise HTTPException(status_code=404, detail="Pizza not found")

    db_pizza.name = pizza.name
    db_pizza.description = pizza.description
    db_pizza.price = pizza.price

    db.commit()
    db.refresh(db_pizza)
    return db_pizza


@router.delete("/pizzas/{pizza_id}")
def delete_pizza(pizza_id: int, db: Session = Depends(get_db)):
    pizza = db.query(Pizza).filter(Pizza.id == pizza_id).first()
    if not pizza:
        raise HTTPException(status_code=404, detail="Pizza not found")

    db.delete(pizza)
    db.commit()
    return {"message": "Pizza deleted successfully"}


@router.get("/pizzas/", response_model=List[PizzaResponse])
def read_all_pizzas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    pizzas = db.query(Pizza).offset(skip).limit(limit).all()
    return pizzas