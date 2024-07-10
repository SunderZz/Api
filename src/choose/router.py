from database import get_db
from .schema import ChooseBase
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from .repository import ChooseRepository
from .services import (
    get_chooses_service,
    get_choose_by_id_service,
    create_choose_service,
    update_choose_service,
)

router = APIRouter(tags=["choose"])


@router.get("/choose/", status_code=status.HTTP_200_OK, response_model=list[ChooseBase])
async def get_chooses(
    choose_repository: ChooseRepository = Depends(ChooseRepository),
    db: AsyncSession = Depends(get_db),
) -> list[ChooseBase]:
    return await get_chooses_service(choose_repository, db)


@router.get(
    "/choose/{choose_id}", status_code=status.HTTP_200_OK, response_model=ChooseBase
)
async def get_choose_by_id(
    choose_id: int,
    choose_repository: ChooseRepository = Depends(ChooseRepository),
    db: AsyncSession = Depends(get_db),
) -> ChooseBase:
    return await get_choose_by_id_service(choose_id, choose_repository, db)


@router.post("/choose/", status_code=status.HTTP_201_CREATED, response_model=ChooseBase)
async def create_choose(
    choose: ChooseBase,
    choose_repository: ChooseRepository = Depends(ChooseRepository),
    db: AsyncSession = Depends(get_db),
) -> ChooseBase:
    return await create_choose_service(choose, choose_repository, db)


@router.put(
    "/choose/{choose_id}", status_code=status.HTTP_200_OK, response_model=ChooseBase
)
async def update_choose(
    choose_id: int,
    choose: ChooseBase,
    choose_repository: ChooseRepository = Depends(ChooseRepository),
    db: AsyncSession = Depends(get_db),
) -> ChooseBase:
    return await update_choose_service(choose_id, choose, choose_repository, db)
