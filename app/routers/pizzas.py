from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import crud, schemas, database

router = APIRouter(prefix="/pizzas", tags=["pizzas"])

@router.get("/", response_model=List[schemas.PizzaBase])
def read_pizzas(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    return crud.get_pizzas(db, skip=skip, limit=limit)