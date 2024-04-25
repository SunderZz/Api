import unit.models as models
import main as get_db
from typing import Annotated
from .schema import UnitBase, UnitValueSchema
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from database import engine, SessionLocal
from .repository import UnitRepository
from common import model_to_dict

def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close_all()

router = APIRouter(tags=["unit"])

models.Base.metadata.create_all(bind=engine)

db_dependency= Annotated[Session, Depends(get_db)]


@router.get("/unit/", status_code=status.HTTP_200_OK, response_model=UnitBase)
async def get_units(unit_repository: UnitRepository = Depends(UnitRepository),db: Session = Depends(get_db))-> UnitBase:
    units = await unit_repository.get_units(db)
    unit_dict = model_to_dict(units) 
    return UnitBase(**unit_dict)


@router.get("/unit/{query}", response_model=UnitValueSchema)
async def get_unit_value(query: str, unit_repository: UnitRepository = Depends(UnitRepository), db: Session = Depends(get_db)) -> UnitValueSchema:
    value = await unit_repository.get_unit_query(db, query)
    if value is None:
        raise HTTPException(status_code=404, detail="Unit not found or attribute not found")
    return UnitValueSchema(value=value)


@router.post("/unit/", status_code=status.HTTP_201_CREATED, response_model=UnitBase)
async def create_unit(unit: UnitBase,unit_repository: UnitRepository = Depends(UnitRepository), db: Session = Depends(get_db))-> UnitBase:
    new_unit = await unit_repository.create_unit(db, unit)
    unit_dict = model_to_dict(new_unit) 
    return UnitBase(**unit_dict)

@router.put("/unit/{unit_id}", status_code=status.HTTP_200_OK, response_model=UnitBase)
async def update_unit(unit_id: int, unit: UnitBase,unit_repository: UnitRepository = Depends(UnitRepository), db: Session = Depends(get_db))-> UnitBase:
    updated_unit = await unit_repository.update_unit(db, unit_id, unit)
    if updated_unit is None:
        raise HTTPException(status_code=404, detail="Unit not found")
    unit_dict = model_to_dict(updated_unit) 
    return UnitBase(**unit_dict)