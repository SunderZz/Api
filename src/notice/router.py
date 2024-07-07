from .schema import NoticeBase, NoticeCreateBase
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from .repository import NoticeRepository
from .services import (
    get_notices_service,
    get_notices_by_id_service,
    create_notice_service,
)

router = APIRouter(tags=["notice"])


@router.get(
    "/notices/", status_code=status.HTTP_200_OK, response_model=list[NoticeBase]
)
async def get_notices(
    notice_repository: NoticeRepository = Depends(NoticeRepository),
    db: AsyncSession = Depends(get_db),
) -> list[NoticeBase]:
    return await get_notices_service(notice_repository, db)


@router.get(
    "/notice/{notice_id}",
    status_code=status.HTTP_200_OK,
    response_model=NoticeBase,
)
async def get_notices_by_id(
    notice_id: int,
    notice_repository: NoticeRepository = Depends(NoticeRepository),
    db: AsyncSession = Depends(get_db),
) -> NoticeBase:
    return await get_notices_by_id_service(notice_id, notice_repository, db)


@router.post(
    "/notice/", status_code=status.HTTP_201_CREATED, response_model=NoticeCreateBase
)
async def create_notice(
    notice: NoticeBase,
    notice_repository: NoticeRepository = Depends(NoticeRepository),
    db: AsyncSession = Depends(get_db),
) -> NoticeCreateBase:
    return await create_notice_service(notice, notice_repository, db)
