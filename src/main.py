from fastapi import APIRouter, FastAPI, Depends
from typing import Annotated
from database import AsyncSessionLocal
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.types import ASGIApp
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from admin.router import router as admin_router
from adresse_types.router import router as adresse_types_router
from asso_33.router import router as asso_33_router
from asso_34.router import router as asso_34_router
from city.router import router as city_router
from carry_on.router import router as carry_on_router
from choose.router import router as choose_router
from code_postal.router import router as code_postal_router
from customers.router import router as customers_router
from found.router import router as found_router
from give.router import router as give_router
from give_1.router import router as give_1_router
from given.router import router as given_router
from got_3.router import router as got_router
from is_on.router import router as ison_router
from linede.router import router as linede_router
from located.router import router as located_router
from manage.router import router as manage_router
from méteo.router import router as méteo_router
from notice.router import router as notice_router
from operate.router import router as operate_router
from orders.router import router as orders_router
from pay.router import router as pay_router
from payement.router import router as payement_router
from preference_ship.router import router as preference_ship_router
from producers.router import router as producers_router
from products.router import router as products_router
from produit_image_1.router import router as produit_image_router
from recipes.router import router as recipes_router
from redac.router import router as redact_router
from season.router import router as season_router
from shipment_cost.router import router as shipment_cost_router
from tva.router import router as tva_router
from unit.router import router as unit_router
from users.router import router as users_router
from users_adresses.router import router as users_adresses_router


app = FastAPI(
    title="API",
)

origins = [
    "http://localhost:8080",
    "http://localhost:5173",
    "http://localhost:8081",
    "https://meteo.francetvinfo.fr/previsions-meteo-outremer/la-reunion",
    "exp://192.168.1.14:8081",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(GZipMiddleware, minimum_size=1000)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

db_dependency = Annotated[AsyncSession, Depends(get_db)]

app.include_router(admin_router)
app.include_router(adresse_types_router)
app.include_router(asso_33_router)
app.include_router(asso_34_router)
app.include_router(city_router)
app.include_router(carry_on_router)
app.include_router(choose_router)
app.include_router(code_postal_router)
app.include_router(customers_router)
app.include_router(found_router)
app.include_router(give_router)
app.include_router(give_1_router)
app.include_router(given_router)
app.include_router(got_router)
app.include_router(ison_router)
app.include_router(linede_router)
app.include_router(located_router)
app.include_router(manage_router)
app.include_router(méteo_router)
app.include_router(notice_router)
app.include_router(operate_router)
app.include_router(orders_router)
app.include_router(pay_router)
app.include_router(payement_router)
app.include_router(preference_ship_router)
app.include_router(producers_router)
app.include_router(products_router)
app.include_router(produit_image_router)
app.include_router(recipes_router)
app.include_router(redact_router)
app.include_router(season_router)
app.include_router(shipment_cost_router)
app.include_router(tva_router)
app.include_router(unit_router)
app.include_router(users_router)
app.include_router(users_adresses_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
