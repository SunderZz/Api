from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from .repository import GivenRepository
from .schema import GivenBase
from common import model_to_dict
from notice.repository import NoticeRepository
from notice.router import create_notice
from notice.schema import NoticeBase
from give_1.repository import Give_1Repository
from give_1.router import create_Give_notice
from give_1.schema import Give_1Base


async def get_givens_service(
    given_repository: GivenRepository, db: AsyncSession
) -> list[GivenBase]:
    givens = await given_repository.get_given(db)
    givens_list = [model_to_dict(given) for given in givens]
    return [GivenBase(**given_dict) for given_dict in givens_list]


async def get_given_by_id_service(
    given_id: int, given_repository: GivenRepository, db: AsyncSession
) -> GivenBase:
    given = await given_repository.get_given_by_id(db, given_id)
    if given is None:
        raise HTTPException(status_code=404, detail="given not found")
    return GivenBase(**model_to_dict(given))


async def get_notice_by_product_service(
    product: int,
    given_repository: GivenRepository,
    notice_repository: NoticeRepository,
    db: AsyncSession,
) -> list[NoticeBase] | None:
    given = await given_repository.get_notice_by_product(db, product)
    if given is None:
        return None
    if isinstance(given, list):
        notices = []
        for giv in given:
            notice = await get_notices_by_id_service(
                giv.Id_Notice, notice_repository, db
            )
            if notice:
                notices.append(notice)
        return notices if notices else None


async def get_notices_by_id_service(
    notice_id: int, notice_repository: NoticeRepository, db: AsyncSession
) -> NoticeBase:
    notice = await notice_repository.get_notice_by_id(db, notice_id)
    if notice:
        notice_dict = model_to_dict(notice)
        return NoticeBase(**notice_dict)
    raise HTTPException(status_code=404, detail="Notice not found")


async def create_notice_for_product_service(
    id_customer: int,
    notice: NoticeBase,
    product: int,
    given_repository: GivenRepository,
    Give_1_repository: Give_1Repository,
    notice_repository: NoticeRepository,
    db: AsyncSession,
) -> GivenBase:
    notice_posted = await create_notice(notice, notice_repository, db)
    new_given = await given_repository.create_given(
        db, GivenBase(Id_Notice=notice_posted.Id_Notice, Id_Product=product)
    )
    await create_Give_notice(
        Give_1Base(Id_Casual=id_customer, Id_Notice=new_given.Id_Notice),
        Give_1_repository,
        db,
    )
    given_dict = model_to_dict(new_given)
    return GivenBase(**given_dict)


async def update_given_service(
    given_id: int, given: GivenBase, given_repository: GivenRepository, db: AsyncSession
) -> GivenBase:
    updated_given = await given_repository.update_given(db, given_id, given)
    if updated_given is None:
        raise HTTPException(status_code=404, detail="given not found")
    return GivenBase(**model_to_dict(updated_given))
