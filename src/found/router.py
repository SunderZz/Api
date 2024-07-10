from database import get_db
from .schema import FoundBase
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from .repository import FoundRepository
from .services import (
    get_founds_service,
    get_found_by_id_service,
    create_found_service,
    update_found_service
)

router = APIRouter(tags=["found"])

@router.get("/found/", status_code=status.HTTP_200_OK, response_model=list[FoundBase])
async def get_founds(
    found_repository: FoundRepository = Depends(FoundRepository),
    db: AsyncSession = Depends(get_db),
) -> list[FoundBase]:
    return await get_founds_service(found_repository, db)

@router.get("/found/{found_id}", status_code=status.HTTP_200_OK, response_model=FoundBase)
async def get_found_by_id(
    found_id: int,
    found_repository: FoundRepository = Depends(FoundRepository),
    db: AsyncSession = Depends(get_db),
) -> FoundBase:
    return await get_found_by_id_service(found_id, found_repository, db)

@router.post("/found/", status_code=status.HTTP_201_CREATED, response_model=FoundBase)
async def create_found(
    found: FoundBase,
    found_repository: FoundRepository = Depends(FoundRepository),
    db: AsyncSession = Depends(get_db),
) -> FoundBase:
    return await create_found_service(found, found_repository, db)

@router.put("/found/{found_id}", status_code=status.HTTP_200_OK, response_model=FoundBase)
async def update_found(
    found_id: int,
    found: FoundBase,
    found_repository: FoundRepository = Depends(FoundRepository),
    db: AsyncSession = Depends(get_db),
) -> FoundBase:
    return await update_found_service(found_id, found, found_repository, db)
