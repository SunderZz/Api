import season.models as models
from database import get_db
from typing import Annotated
from .schema import ChooseBase
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import engine2, AsyncSessionLocal
from .repository import ChooseRepository
from common import model_to_dict


router = APIRouter(tags=["chooseose"])


@router.get("/choose/", status_code=status.HTTP_200_OK, response_model=list[ChooseBase])
async def get_chooseoses(
    choose_repository: ChooseRepository = Depends(ChooseRepository),
    db: AsyncSession = Depends(get_db),
) -> list[ChooseBase]:
    chooses = await choose_repository.get_choose(db)
    chooses_list = [model_to_dict(choose) for choose in chooses]
    return [ChooseBase(**choose_dict) for choose_dict in chooses_list]


@router.get(
    "/choose/{choose_id}", status_code=status.HTTP_200_OK, response_model=ChooseBase
)
async def get_chooseose_by_id(
    choose_id: int,
    choose_repository: ChooseRepository = Depends(ChooseRepository),
    db: AsyncSession = Depends(get_db),
) -> ChooseBase:
    choose = await choose_repository.get_choose_by_id(db, choose_id)
    if choose is None:
        raise HTTPException(status_code=404, detail="choose not choose")
    return ChooseBase(**model_to_dict(choose))


@router.post("/choose/", status_code=status.HTTP_201_CREATED, response_model=ChooseBase)
async def create_choose(
    choose: ChooseBase,
    choose_repository: ChooseRepository = Depends(ChooseRepository),
    db: AsyncSession = Depends(get_db),
) -> ChooseBase:
    new_choose = await choose_repository.create_choose(db, choose)
    choose_dict = model_to_dict(new_choose)
    return ChooseBase(**choose_dict)


@router.put(
    "/choose/{choose_id}", status_code=status.HTTP_200_OK, response_model=ChooseBase
)
async def update_choose(
    choose_id: int,
    choose: ChooseBase,
    choose_repository: ChooseRepository = Depends(ChooseRepository),
    db: AsyncSession = Depends(get_db),
) -> ChooseBase:
    updated_choose = await choose_repository.update_choose(db, choose_id, choose)
    if updated_choose is None:
        raise HTTPException(status_code=404, detail="choose not choose")
    choose_dict = model_to_dict(updated_choose)
    return ChooseBase(**choose_dict)
