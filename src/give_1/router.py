import give_1.models as models
from database import get_db
from typing import Annotated
from .schema import Give_1Base
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import engine2, AsyncSessionLocal
from .repository import Give_1Repository
from common import model_to_dict


router = APIRouter(tags=["give_1"])

@router.get("/Give_1/", status_code=status.HTTP_200_OK, response_model=list[Give_1Base])
async def get_Give_1s(Give_1_repository: Give_1Repository = Depends(Give_1Repository), db:AsyncSession = Depends(get_db)) -> list[Give_1Base]:
    Give_1s = await Give_1_repository.get_give_1(db)
    Give_1s_list = [model_to_dict(Give_1) for Give_1 in Give_1s]
    return [Give_1Base(**Give_1_dict) for Give_1_dict in Give_1s_list]

@router.get("/Give_1/{Give_1_id}", status_code=status.HTTP_200_OK, response_model=Give_1Base)
async def get_Give_1_by_id(Give_1_id: int, Give_1_repository: Give_1Repository = Depends(Give_1Repository), db:AsyncSession = Depends(get_db)) -> Give_1Base:
    Give_1 = await Give_1_repository.get_give_1_by_id(db, Give_1_id)
    if Give_1 is None:
        raise HTTPException(status_code=404, detail="Give_1 not found")
    return Give_1Base(**model_to_dict(Give_1))

@router.post("/Give_1/", status_code=status.HTTP_201_CREATED, response_model=Give_1Base)
async def create_Give_notice(Give_1: Give_1Base, Give_1_repository: Give_1Repository = Depends(Give_1Repository), db:AsyncSession = Depends(get_db)) -> Give_1Base:
    new_Give_1 = await Give_1_repository.create_give_1(db, Give_1)
    Give_1_dict = model_to_dict(new_Give_1)
    return Give_1Base(**Give_1_dict)

@router.put("/Give_1/{Give_1_id}", status_code=status.HTTP_200_OK, response_model=Give_1Base)
async def update_Give_1(Give_1_id: int, Give_1: Give_1Base, Give_1_repository: Give_1Repository = Depends(Give_1Repository), db:AsyncSession = Depends(get_db)) -> Give_1Base:
    updated_Give_1 = await Give_1_repository.update_give_1(db, Give_1_id, Give_1)
    if updated_Give_1 is None:
        raise HTTPException(status_code=404, detail="Give_1 not found")
    Give_1_dict = model_to_dict(updated_Give_1)
    return Give_1Base(**Give_1_dict)
