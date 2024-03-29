from fastapi import APIRouter, FastAPI, Depends
from typing import Annotated
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from starlette.types import ASGIApp

from fastapi.middleware.gzip import GZipMiddleware

from admin.router import router as admin_router
from adresse_types.router import router as adresse_types_router
from casual_5.router import router as casual_5_router
from city.router import router as city_router
from code_postal.router import router as code_postal_router
from customers.router import router as customers_router
from notice.router import router as notice_router
from orders.router import router as orders_router
from payement.router import router as payement_router
from preference_ship.router import router as preference_ship_router
from producers.router import router as producers_router
from products.router import router as products_router
from produit_image_1.router import router as image_router
from recipes.router import router as recipes_router
from season.router import router as season_router
from shipment_cost.router import router as shipment_cost_router
from tva.router import router as tva_router
from unit.router import router as unit_router
from users.router import router as users_router
from users_adresses.router import router as users_adresses_router

app = FastAPI(
    title="API",
)

fallback_url_router = APIRouter(tags=["fallback_url"])
CAPACITOR_ORIGIN = "http://localhost"


class ContentTypeMiddleware:
    def __init__(self, app: ASGIApp, default: str):
        self.app = app
        self.default = default


def get_db():
    db = SessionLocal
    try: 
        yield db
    finally:
        db.close_all()

db_dependency= Annotated[Session, Depends(get_db)]



app.add_middleware(GZipMiddleware, minimum_size=1000)

app.include_router(admin_router)
app.include_router(adresse_types_router)
app.include_router(casual_5_router)
app.include_router(city_router)
app.include_router(code_postal_router)
app.include_router(customers_router)
app.include_router(image_router)
app.include_router(notice_router)
app.include_router(orders_router)
app.include_router(payement_router)
app.include_router(preference_ship_router)
app.include_router(producers_router)
app.include_router(products_router)
app.include_router(recipes_router)
app.include_router(season_router)
app.include_router(shipment_cost_router)
app.include_router(tva_router)
app.include_router(unit_router)
app.include_router(users_router)
app.include_router(users_adresses_router)



