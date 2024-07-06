import asso_34.models as models
from database import get_db
from typing import Annotated
from .schema import Asso_34Base
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import engine2, AsyncSessionLocal
from .repository import Asso_34Repository
from common import model_to_dict

router = APIRouter(tags=["asso_34"])


@router.get(
    "/asso_34/", status_code=status.HTTP_200_OK, response_model=list[Asso_34Base]
)
async def get_asso_34oses(
    asso_34_repository: Asso_34Repository = Depends(Asso_34Repository),
    db: AsyncSession = Depends(get_db),
) -> list[Asso_34Base]:
    asso_34s = await asso_34_repository.get_asso_34(db)
    asso_34s_list = [model_to_dict(asso_34) for asso_34 in asso_34s]
    return [Asso_34Base(**asso_34_dict) for asso_34_dict in asso_34s_list]


@router.get(
    "/asso_34/{asso_34_id}", status_code=status.HTTP_200_OK, response_model=Asso_34Base
)
async def get_asso_34ose_by_id(
    asso_34_id: int,
    asso_34_repository: Asso_34Repository = Depends(Asso_34Repository),
    db: AsyncSession = Depends(get_db),
) -> Asso_34Base:
    asso_34 = await asso_34_repository.get_asso_34_by_id(db, asso_34_id)
    if asso_34 is None:
        raise HTTPException(status_code=404, detail="asso_34 not asso_34")
    return Asso_34Base(**model_to_dict(asso_34))


@router.post(
    "/asso_34/", status_code=status.HTTP_201_CREATED, response_model=Asso_34Base
)
async def create_asso_34(
    asso_34: Asso_34Base,
    asso_34_repository: Asso_34Repository = Depends(Asso_34Repository),
    db: AsyncSession = Depends(get_db),
) -> Asso_34Base:
    new_asso_34 = await asso_34_repository.create_asso_34(db, asso_34)
    asso_34_dict = model_to_dict(new_asso_34)
    return Asso_34Base(**asso_34_dict)


@router.put(
    "/asso_34/{asso_34_id}", status_code=status.HTTP_200_OK, response_model=Asso_34Base
)
async def update_asso_34(
    asso_34_id: int,
    asso_34: Asso_34Base,
    asso_34_repository: Asso_34Repository = Depends(Asso_34Repository),
    db: AsyncSession = Depends(get_db),
) -> Asso_34Base:
    updated_asso_34 = await asso_34_repository.update_asso_34(db, asso_34_id, asso_34)
    if updated_asso_34 is None:
        raise HTTPException(status_code=404, detail="asso_34 not asso_34")
    asso_34_dict = model_to_dict(updated_asso_34)
    return Asso_34Base(**asso_34_dict)
