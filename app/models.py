from datetime import datetime
from xmlrpc.client import DateTime

from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, JSON, DateTime, func
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)

class Pizza(Base):
    __tablename__ = 'pizzas'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    description = Column(String)
    price = Column(Float)
    is_active = Column(Boolean, default=True)

class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True, index=True)
    pizza_id = Column(Integer)
    customer_name = Column(String)
    address = Column(String)
    status = Column(String, default='pending')

class Cart(Base):
    __tablename__ = "carts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    items = Column(JSON, default=[])
    created_at = Column(DateTime, default=datetime)
    updated_at = Column(DateTime, default=datetime, onupdate=datetime)

