from database import get_db
from .schema import ManageBase
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from .repository import ManageRepository
from .services import (
    get_manages_service,
    get_manage_by_id_service,
    create_manage_service,
)

router = APIRouter(tags=["manage"])


@router.get("/manage/", status_code=status.HTTP_200_OK, response_model=list[ManageBase])
async def get_manages(
    manage_repository: ManageRepository = Depends(ManageRepository),
    db: AsyncSession = Depends(get_db),
) -> list[ManageBase]:
    return await get_manages_service(manage_repository, db)


@router.get(
    "/manage/{manage_id}", status_code=status.HTTP_200_OK, response_model=ManageBase
)
async def get_manage_by_id(
    manage_id: int,
    manage_repository: ManageRepository = Depends(ManageRepository),
    db: AsyncSession = Depends(get_db),
) -> ManageBase:
    return await get_manage_by_id_service(manage_id, manage_repository, db)


@router.post("/manage/", status_code=status.HTTP_201_CREATED, response_model=ManageBase)
async def create_manage(
    manage: ManageBase,
    manage_id: int,
    manage_repository: ManageRepository = Depends(ManageRepository),
    db: AsyncSession = Depends(get_db),
) -> ManageBase:
    return await create_manage_service(manage, manage_id, manage_repository, db)
