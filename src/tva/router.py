import tva.models as models
from typing import Annotated
from .schema import TvaBase, TvaCalculationResult
from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from database import engine2, AsyncSessionLocal
from .repository import TvaRepository
from common import model_to_dict

router = APIRouter(tags=["tva"])

@router.get("/tva/{tva_id}", response_model=TvaBase)
async def get_tva(tva_id: int, tva_repository: TvaRepository = Depends(TvaRepository), db:AsyncSession = Depends(get_db))->TvaBase:
    tva = await tva_repository.get_tva(db, tva_id)
    if tva is None:
        raise HTTPException(status_code=404, detail="Tva not found")
    tva_dict = model_to_dict(tva) 
    return TvaBase(**tva_dict)

@router.get("/tva_name/{tva_id}", response_model=TvaBase)
async def get_tva_with_name(tva_id: str, tva_repository: TvaRepository = Depends(TvaRepository), db:AsyncSession = Depends(get_db))->TvaBase:
    tva = await tva_repository.get_tva_by_name(db, tva_id)
    if tva is None:
        raise HTTPException(status_code=404, detail="Tva not found")
    tva_dict = model_to_dict(tva) 
    return TvaBase(**tva_dict)

@router.get("/tva/calculate/{tva_name}", response_model=TvaCalculationResult)
async def calculate_tva(tva_name: str, price: float, db:AsyncSession = Depends(get_db), tva_repository: TvaRepository = Depends(TvaRepository))->TvaCalculationResult:
    tva_value = await tva_repository.calculate_tva(db, price, tva_name)
    if tva_value is None:
        raise HTTPException(status_code=404, detail="Tva not found")
    return TvaCalculationResult(value=tva_value)

@router.get("/tva", status_code=status.HTTP_200_OK, response_model=list[TvaBase])
async def get_all_tva(tva_repository: TvaRepository = Depends(TvaRepository),db:AsyncSession = Depends(get_db))-> list[TvaBase]:
    Tva = await tva_repository.get_all_tva(db)
    tvas_list = [model_to_dict(tvas) for tvas in Tva]
    return [TvaBase(**tva_dict) for tva_dict in tvas_list]


@router.put("/tva/{tva_id}", response_model=TvaBase)
async def update_tva(tva_id: int, tva: TvaBase,  tva_repository: TvaRepository = Depends(TvaRepository), db:AsyncSession = Depends(get_db))->TvaBase:
    updated_tva = await tva_repository.update_tva(db, tva, tva_id)
    if updated_tva is None:
        raise HTTPException(status_code=404, detail="Tva not found")
    tva_dict = model_to_dict(updated_tva) 
    return TvaBase(**tva_dict)

@router.post("/tva/", response_model=TvaBase)
async def create_tva(tva: TvaBase, tva_repository: TvaRepository = Depends(TvaRepository), db:AsyncSession = Depends(get_db))->TvaBase:
    created_tva = await tva_repository.create_tva(db, tva)
    tva_dict = model_to_dict(created_tva) 
    return TvaBase(**tva_dict)
