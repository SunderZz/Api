import asso_33.models as models
from database import get_db
from typing import Annotated
from .schema import Asso_33Base
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import engine2, AsyncSessionLocal
from .repository import Asso_33Repository
from common import model_to_dict

def get_db():
    db = AsyncSessionLocal()
    try: 
        yield db
    finally:
        db.close_all()

router = APIRouter(tags=["asso_33"])


@router.get("/asso_33/", status_code=status.HTTP_200_OK, response_model=list[Asso_33Base])
async def get_asso_33oses(asso_33_repository: Asso_33Repository = Depends(Asso_33Repository), db:AsyncSession = Depends(get_db)) -> list[Asso_33Base]:
    asso_33s = await asso_33_repository.get_asso_33(db)
    asso_33s_list = [model_to_dict(asso_33) for asso_33 in asso_33s]
    return [Asso_33Base(**asso_33_dict) for asso_33_dict in asso_33s_list]

@router.get("/asso_33/{asso_33_id}", status_code=status.HTTP_200_OK, response_model=Asso_33Base)
async def get_asso_33ose_by_id(asso_33_id: int, asso_33_repository: Asso_33Repository = Depends(Asso_33Repository), db:AsyncSession = Depends(get_db)) -> Asso_33Base:
    asso_33 = await asso_33_repository.get_asso_33_by_id(db, asso_33_id)
    if asso_33 is None:
        raise HTTPException(status_code=404, detail="asso_33 not asso_33")
    return Asso_33Base(**model_to_dict(asso_33))

@router.post("/asso_33/", status_code=status.HTTP_201_CREATED, response_model=Asso_33Base)
async def create_asso_33(asso_33: Asso_33Base, asso_33_repository: Asso_33Repository = Depends(Asso_33Repository), db:AsyncSession = Depends(get_db)) -> Asso_33Base:
    new_asso_33 = await asso_33_repository.create_asso_33(db, asso_33)
    asso_33_dict = model_to_dict(new_asso_33)
    return Asso_33Base(**asso_33_dict)

@router.put("/asso_33/{asso_33_id}", status_code=status.HTTP_200_OK, response_model=Asso_33Base)
async def update_asso_33(asso_33_id: int, asso_33: Asso_33Base, asso_33_repository: Asso_33Repository = Depends(Asso_33Repository), db:AsyncSession = Depends(get_db)) -> Asso_33Base:
    updated_asso_33 = await asso_33_repository.update_asso_33(db, asso_33_id, asso_33)
    if updated_asso_33 is None:
        raise HTTPException(status_code=404, detail="asso_33 not asso_33")
    asso_33_dict = model_to_dict(updated_asso_33)
    return Asso_33Base(**asso_33_dict)
