from database import get_db
from .schema import GiveBase, GiveCalcBase
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from .repository import GiveRepository
from .services import (
    get_gives_service,
    get_give_by_id_service,
    get_give_by_id_producers_service,
    create_give_service,
    update_give_service,
)

router = APIRouter(tags=["give"])


@router.get("/give/", status_code=status.HTTP_200_OK, response_model=list[GiveBase])
async def get_gives(
    give_repository: GiveRepository = Depends(GiveRepository),
    db: AsyncSession = Depends(get_db),
) -> list[GiveBase]:
    return await get_gives_service(give_repository, db)


@router.get("/give/{give_id}", status_code=status.HTTP_200_OK, response_model=GiveBase)
async def get_give_by_id(
    give_id: int,
    give_repository: GiveRepository = Depends(GiveRepository),
    db: AsyncSession = Depends(get_db),
) -> GiveBase:
    return await get_give_by_id_service(give_id, give_repository, db)


@router.get(
    "/give_producers", status_code=status.HTTP_200_OK, response_model=list[GiveBase]
)
async def get_give_by_id_producers(
    give_id: int,
    give_repository: GiveRepository = Depends(GiveRepository),
    db: AsyncSession = Depends(get_db),
) -> list[GiveBase]:
    return await get_give_by_id_producers_service(give_id, give_repository, db)


@router.post("/give/", status_code=status.HTTP_201_CREATED, response_model=GiveBase)
async def create_give(
    give: GiveBase,
    give_repository: GiveRepository = Depends(GiveRepository),
    db: AsyncSession = Depends(get_db),
) -> GiveBase:
    return await create_give_service(give, give_repository, db)


@router.put("/give/{give_id}", status_code=status.HTTP_200_OK, response_model=GiveBase)
async def update_give(
    give_id: int,
    give: GiveCalcBase,
    give_repository: GiveRepository = Depends(GiveRepository),
    db: AsyncSession = Depends(get_db),
) -> GiveBase:
    return await update_give_service(give_id, give, give_repository, db)
