from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from .repository import NoticeRepository
from .schema import NoticeBase, NoticeCreateBase
from common import model_to_dict


async def get_notices_service(
    notice_repository: NoticeRepository, db: AsyncSession
) -> list[NoticeBase]:
    notices = await notice_repository.get_notice(db)
    notice_list = [model_to_dict(notice) for notice in notices]
    return [NoticeBase(**notice_dict) for notice_dict in notice_list]


async def get_notices_by_id_service(
    notice_id: int, notice_repository: NoticeRepository, db: AsyncSession
) -> list[NoticeBase] | NoticeBase | None:
    notices = await notice_repository.get_notice_by_id(db, notice_id)
    if notices is None:
        raise HTTPException(status_code=404, detail="Notice not found")
    return NoticeBase(**model_to_dict(notices))


async def create_notice_service(
    notice: NoticeBase, notice_repository: NoticeRepository, db: AsyncSession
) -> NoticeCreateBase:
    new_notice = await notice_repository.create_notice(db, notice)
    notice_dict = model_to_dict(new_notice)
    return NoticeCreateBase(**notice_dict)
