from database import get_db
from .schema import LocatedBase
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from .repository import LocatedRepository
from .services import (
    get_locateds_service,
    get_located_by_ids_service,
    create_located_service,
    update_located_service,
)

router = APIRouter(tags=["located"])


@router.get(
    "/located/", status_code=status.HTTP_200_OK, response_model=list[LocatedBase]
)
async def get_locateds(
    located_repository: LocatedRepository = Depends(LocatedRepository),
    db: AsyncSession = Depends(get_db),
) -> list[LocatedBase]:
    return await get_locateds_service(located_repository, db)


@router.get(
    "/located/{located_id}", status_code=status.HTTP_200_OK, response_model=LocatedBase
)
async def get_located_by_ids(
    located_id: int,
    located_repository: LocatedRepository = Depends(LocatedRepository),
    db: AsyncSession = Depends(get_db),
) -> LocatedBase:
    return await get_located_by_ids_service(located_id, located_repository, db)


@router.post(
    "/located/", status_code=status.HTTP_201_CREATED, response_model=LocatedBase
)
async def create_located(
    located: LocatedBase,
    located_repository: LocatedRepository = Depends(LocatedRepository),
    db: AsyncSession = Depends(get_db),
) -> LocatedBase:
    return await create_located_service(located, located_repository, db)


@router.put(
    "/located/{located_id}", status_code=status.HTTP_200_OK, response_model=LocatedBase
)
async def update_located(
    located_id: int,
    located: LocatedBase,
    located_repository: LocatedRepository = Depends(LocatedRepository),
    db: AsyncSession = Depends(get_db),
) -> LocatedBase:
    return await update_located_service(located_id, located, located_repository, db)
