import shipment_cost.models as models
from typing import Annotated
from .schema import ShipmentsCostBase
from fastapi import APIRouter, FastAPI, Depends, status
from sqlalchemy.orm import Session
import main as get_db
from database import engine, SessionLocal


def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close_all()

router = APIRouter(tags=["shipment_cost"])

models.Base.metadata.create_all(bind=engine)

db_dependency= Annotated[Session, Depends(get_db)]


@router.get("/shipment/", status_code= status.HTTP_201_CREATED)
async def get_shipment(db: db_dependency):
    shipment= db.query(models.Shipments_Cost).all()
    # +func de calcul
    return {"shipment":shipment}

@router.put("/shipment/", status_code= status.HTTP_201_CREATED)
async def put_shipment(db: db_dependency):
    shipment= db.query(models.Shipments_Cost).all()
    return {"shipment":shipment}

#get shipment cost
# post shipment cost
# put shipment cost
# get calculate shipment cost