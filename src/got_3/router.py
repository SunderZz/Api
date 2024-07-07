from database import get_db
from .schema import GotBase
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from .repository import GotRepository
from .services import (
    get_gots_service,
    get_got_by_id_service,
    create_got_service,
    update_got_service,
)

router = APIRouter(tags=["got"])


@router.get("/got/", status_code=status.HTTP_200_OK, response_model=list[GotBase])
async def get_gots(
    got_repository: GotRepository = Depends(GotRepository),
    db: AsyncSession = Depends(get_db),
) -> list[GotBase]:
    return await get_gots_service(got_repository, db)


@router.get(
    "/got/{got_id}",
    status_code=status.HTTP_200_OK,
    response_model=GotBase | list[GotBase],
)
async def get_got_by_id(
    got_id: int,
    got_repository: GotRepository = Depends(GotRepository),
    db: AsyncSession = Depends(get_db),
) -> GotBase | list[GotBase]:
    return await get_got_by_id_service(got_id, got_repository, db)


@router.post("/got/", status_code=status.HTTP_201_CREATED, response_model=GotBase)
async def create_got(
    got: GotBase,
    got_repository: GotRepository = Depends(GotRepository),
    db: AsyncSession = Depends(get_db),
) -> GotBase:
    return await create_got_service(got, got_repository, db)


@router.put("/got/{got_id}", status_code=status.HTTP_200_OK, response_model=GotBase)
async def update_got(
    got: GotBase,
    got_id: int,
    got_repository: GotRepository = Depends(GotRepository),
    db: AsyncSession = Depends(get_db),
) -> GotBase:
    return await update_got_service(got, got_id, got_repository, db)
