import unit.models as models
from database import get_db
from typing import Annotated
from .schema import UnitBase, UnitIdBase
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import engine2, AsyncSessionLocal
from .repository import UnitRepository
from common import model_to_dict

router = APIRouter(tags=["unit"])

@router.get("/unit/", status_code=status.HTTP_200_OK, response_model=UnitBase)
async def get_units(unit_repository: UnitRepository = Depends(UnitRepository),db:AsyncSession = Depends(get_db))-> UnitBase:
    units = await unit_repository.get_units(db)
    unit_dict = model_to_dict(units) 
    return UnitBase(**unit_dict)


@router.post("/unit/", status_code=status.HTTP_201_CREATED, response_model=UnitIdBase)
async def create_unity(unit: UnitBase,unit_repository: UnitRepository = Depends(UnitRepository), db:AsyncSession = Depends(get_db))-> UnitIdBase:
    new_unit = await unit_repository.create_unit(db, unit)
    unit_dict = model_to_dict(new_unit) 
    return UnitIdBase(**unit_dict)

@router.put("/unit/{unit_id}", status_code=status.HTTP_200_OK, response_model=UnitBase)
async def update_unit(unit_id: int, unit: UnitBase,unit_repository: UnitRepository = Depends(UnitRepository), db:AsyncSession = Depends(get_db))-> UnitBase:
    updated_unit = await unit_repository.update_unit(db, unit_id, unit)
    if updated_unit is None:
        raise HTTPException(status_code=404, detail="Unit not found")
    unit_dict = model_to_dict(updated_unit) 
    return UnitBase(**unit_dict)