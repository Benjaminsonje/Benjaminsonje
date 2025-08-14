from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.db.session import init_db
from app.routers import auth, products, categories, cart, orders, health

app = FastAPI(title="E-commerce API", version="0.1.0")

# CORS
origins = [origin.strip() for origin in settings.CORS_ORIGINS.split(",") if origin.strip()] or ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(health.router, prefix="/health", tags=["health"]) 
app.include_router(auth.router, prefix="/auth", tags=["auth"]) 
app.include_router(categories.router, prefix="/categories", tags=["categories"]) 
app.include_router(products.router, prefix="/products", tags=["products"]) 
app.include_router(cart.router, prefix="/cart", tags=["cart"]) 
app.include_router(orders.router, prefix="/orders", tags=["orders"]) 


@app.on_event("startup")
def on_startup() -> None:
    init_db()