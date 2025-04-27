from typing import List

from pydantic import BaseModel

from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    is_admin: bool

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None

class PizzaBase(BaseModel):
    name: str
    description: str
    price: float


class PizzaCreate(PizzaBase):
    pass


class PizzaResponse(PizzaBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True


class OrderBase(BaseModel):
    pizza_id: int
    customer_name: str
    address: str


class OrderCreate(OrderBase):
    pass


class OrderResponse(OrderBase):
    id: int
    status: str

    class Config:
        from_attributes = True

class CartItem(BaseModel):
    pizza_id: int
    quantity: int

class CartCreate(BaseModel):
    items: List[CartItem] = []

class CartResponse(BaseModel):
    id: int
    items: List[CartItem]
    total: float

    class Config:
        from_attributes = True