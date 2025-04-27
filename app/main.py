from fastapi import FastAPI
from .database import engine, Base
from app.routers import pizzas, orders, admin, cart, auth
from . import models
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(pizzas.router)
app.include_router(orders.router)
app.include_router(admin.router)
app.include_router(auth.router)
app.include_router(cart.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Для разработки, в продакшене укажите конкретный домен
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/app/templates", StaticFiles(directory="app/templates"), name="app/templates")
templates = Jinja2Templates(directory="app/templates")

@app.get("/")
def home():
    return {"test": "ok"}

