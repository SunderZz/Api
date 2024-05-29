import season.models as models
from database import get_db
from typing import Annotated
from .schema import LinedeBase
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import engine2, AsyncSessionLocal
from .repository import LinedeRepository
from common import model_to_dict


router = APIRouter(tags=["linede"])

@router.get("/linede/", status_code=status.HTTP_200_OK, response_model=list[LinedeBase])
async def get_linedes(linede_repository: LinedeRepository = Depends(LinedeRepository), db:AsyncSession = Depends(get_db)) -> list[LinedeBase]:
    linedes = await linede_repository.get_linede(db)
    linedes_list = [model_to_dict(linede) for linede in linedes]
    return [LinedeBase(**linede_dict) for linede_dict in linedes_list]

@router.get("/linede/{linede_id}", status_code=status.HTTP_200_OK, response_model=LinedeBase|list[LinedeBase])
async def get_linede_by_id(linede_id: int, linede_repository: LinedeRepository = Depends(LinedeRepository), db:AsyncSession = Depends(get_db)) -> LinedeBase|list[LinedeBase]:
    linede = await linede_repository.get_linede_by_id(db, linede_id)
    if linede is None:
        raise HTTPException(status_code=404, detail="linede not found")
    if isinstance(linede, list):
        linedes_list = [model_to_dict(line) for line in linede]
        return [LinedeBase(**linede_dict) for linede_dict in linedes_list]
    else:
        linede_dict = model_to_dict(linede)
        return LinedeBase(**linede_dict)

@router.post("/linede/", status_code=status.HTTP_201_CREATED, response_model=LinedeBase)
async def create_linede(linede: LinedeBase, linede_repository: LinedeRepository = Depends(LinedeRepository), db:AsyncSession = Depends(get_db)) -> LinedeBase:
    new_linede = await linede_repository.create_linede(db,linede)
    linede_dict = model_to_dict(new_linede)
    return LinedeBase(**linede_dict)

@router.post("/linede/orders", status_code=status.HTTP_201_CREATED, response_model=LinedeBase | list[LinedeBase])
async def create_linede_for_order(linede: LinedeBase |list[LinedeBase], linede_repository: LinedeRepository = Depends(LinedeRepository), db:AsyncSession = Depends(get_db)) -> LinedeBase | list[LinedeBase]:
    new_linede = await linede_repository.add_products_to_order(db,linede)
    if isinstance(new_linede,list):
        linedes_list = [model_to_dict(linede) for linede in new_linede]
        return [LinedeBase(**linede_dict) for linede_dict in linedes_list]
    else:
        linede_dict = model_to_dict(new_linede)
        return LinedeBase(**linede_dict)

@router.put("/linede/{linede_id}", status_code=status.HTTP_200_OK, response_model=LinedeBase)
async def update_linede(linede_id: int, linede: LinedeBase, linede_repository: LinedeRepository = Depends(LinedeRepository), db:AsyncSession = Depends(get_db)) -> LinedeBase:
    updated_linede = await linede_repository.update_linede(db, linede_id, linede)
    if updated_linede is None:
        raise HTTPException(status_code=404, detail="linede not found")
    linede_dict = model_to_dict(updated_linede)
    return LinedeBase(**linede_dict)
