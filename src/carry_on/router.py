import season.models as models
import main as get_db
from typing import Annotated
from .schema import CarryOnBase
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from database import engine, SessionLocal
from .repository import CarryOnRepository
from common import model_to_dict

def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close_all()

router = APIRouter(tags=["carry_on"])

models.Base.metadata.create_all(bind=engine)

db_dependency= Annotated[Session, Depends(get_db)]

@router.get("/carry_on/", status_code=status.HTTP_200_OK, response_model=list[CarryOnBase])
async def get_carry_onoses(carry_on_repository: CarryOnRepository = Depends(CarryOnRepository), db: Session = Depends(get_db)) -> list[CarryOnBase]:
    carry_ons = await carry_on_repository.get_carry_on(db)
    carry_ons_list = [model_to_dict(carry_on) for carry_on in carry_ons]
    return [CarryOnBase(**carry_on_dict) for carry_on_dict in carry_ons_list]

@router.get("/carry_on/{carry_on_id}", status_code=status.HTTP_200_OK, response_model=CarryOnBase)
async def get_carry_onose_by_id(carry_on_id: int, carry_on_repository: CarryOnRepository = Depends(CarryOnRepository), db: Session = Depends(get_db)) -> CarryOnBase:
    carry_on = await carry_on_repository.get_carry_on_by_id(db, carry_on_id)
    if carry_on is None:
        raise HTTPException(status_code=404, detail="carry_on not carry_on")
    return CarryOnBase(**model_to_dict(carry_on))

@router.post("/carry_on/", status_code=status.HTTP_201_CREATED, response_model=CarryOnBase)
async def create_carry_on(carry_on: CarryOnBase, carry_on_repository: CarryOnRepository = Depends(CarryOnRepository), db: Session = Depends(get_db)) -> CarryOnBase:
    new_carry_on = await carry_on_repository.create_carry_on(db, carry_on)
    carry_on_dict = model_to_dict(new_carry_on)
    return CarryOnBase(**carry_on_dict)

@router.put("/carry_on/{carry_on_id}", status_code=status.HTTP_200_OK, response_model=CarryOnBase)
async def update_carry_on(carry_on_id: int, carry_on: CarryOnBase, carry_on_repository: CarryOnRepository = Depends(CarryOnRepository), db: Session = Depends(get_db)) -> CarryOnBase:
    updated_carry_on = await carry_on_repository.update_carry_on(db, carry_on_id, carry_on)
    if updated_carry_on is None:
        raise HTTPException(status_code=404, detail="carry_on not carry_on")
    carry_on_dict = model_to_dict(updated_carry_on)
    return CarryOnBase(**carry_on_dict)
