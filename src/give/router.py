import season.models as models
from database import get_db
from typing import Annotated
from .schema import GiveBase, GiveCalcBase
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import engine2, AsyncSessionLocal
from .repository import GiveRepository
from common import model_to_dict

router = APIRouter(tags=["give"])


@router.get("/give/", status_code=status.HTTP_200_OK, response_model=list[GiveBase])
async def get_gives(
    give_repository: GiveRepository = Depends(GiveRepository),
    db: AsyncSession = Depends(get_db),
) -> list[GiveBase]:
    gives = await give_repository.get_give(db)
    gives_list = [model_to_dict(give) for give in gives]
    return [GiveBase(**give_dict) for give_dict in gives_list]


@router.get("/give/{give_id}", status_code=status.HTTP_200_OK, response_model=GiveBase)
async def get_give_by_id(
    give_id: int,
    give_repository: GiveRepository = Depends(GiveRepository),
    db: AsyncSession = Depends(get_db),
) -> GiveBase:
    give = await give_repository.get_give_by_id(db, give_id)
    if give is None:
        raise HTTPException(status_code=404, detail="give not found")
    return GiveBase(**model_to_dict(give))


@router.get(
    "/give_producers", status_code=status.HTTP_200_OK, response_model=list[GiveBase]
)
async def get_give_by_id(
    give_id: int,
    give_repository: GiveRepository = Depends(GiveRepository),
    db: AsyncSession = Depends(get_db),
) -> list[GiveBase]:
    give = await give_repository.get_give_by_id_producers(db, give_id)
    if give is None:
        raise HTTPException(status_code=404, detail="give not found")
    gives_list = [model_to_dict(giveS) for giveS in give]
    return [GiveBase(**give_dict) for give_dict in gives_list]


@router.post("/give/", status_code=status.HTTP_201_CREATED, response_model=GiveBase)
async def create_give(
    give: GiveBase,
    give_repository: GiveRepository = Depends(GiveRepository),
    db: AsyncSession = Depends(get_db),
) -> GiveBase:
    new_give = await give_repository.create_give(db, give)
    give_dict = model_to_dict(new_give)
    return GiveBase(**give_dict)


@router.put("/give/{give_id}", status_code=status.HTTP_200_OK, response_model=GiveBase)
async def update_give(
    give_id: int,
    give: GiveCalcBase,
    give_repository: GiveRepository = Depends(GiveRepository),
    db: AsyncSession = Depends(get_db),
) -> GiveBase:
    updated_give = await give_repository.update_give(db, give_id, give)
    if updated_give is None:
        raise HTTPException(status_code=404, detail="give not found")
    give_dict = model_to_dict(updated_give)
    return GiveBase(**give_dict)
