import users.models as models
from typing import Annotated
from .schema import ShipmentsCostBase
from fastapi import APIRouter, FastAPI, Depends, status
from sqlalchemy.orm import Session
import main as get_db
from database import engine, SessionLocal


def get_db():
    db = SessionLocal
    try: 
        yield db
    finally:
        db.close_all()

router = APIRouter(tags=["shipment_cost"])

models.Base.metadata.create_all(bind=engine)

db_dependency= Annotated[Session, Depends(get_db)]


@router.post("/shipment/", status_code= status.HTTP_201_CREATED)
async def create_user(shipment:ShipmentsCostBase, db: db_dependency):
    db_user= models(**shipment.model_dump())
    db.add(db_user)
    db.commit()