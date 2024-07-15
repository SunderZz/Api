from database import get_db
from .schema import GivenBase
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from .repository import GivenRepository
from .services import (
    get_givens_service,
    get_given_by_id_service,
    get_notice_by_product_service,
    create_notice_for_product_service,
    update_given_service,
)
from notice.repository import NoticeRepository
from give_1.repository import Give_1Repository
from notice.schema import NoticeBase
from notice.router import get_notices_by_id

router = APIRouter(tags=["given"])


@router.get("/given/", status_code=status.HTTP_200_OK, response_model=list[GivenBase])
async def get_givens(
    given_repository: GivenRepository = Depends(GivenRepository),
    db: AsyncSession = Depends(get_db),
) -> list[GivenBase]:
    return await get_givens_service(given_repository, db)


@router.get(
    "/given/{given_id}", status_code=status.HTTP_200_OK, response_model=GivenBase
)
async def get_given_by_id(
    given_id: int,
    given_repository: GivenRepository = Depends(GivenRepository),
    db: AsyncSession = Depends(get_db),
) -> GivenBase:
    return await get_given_by_id_service(given_id, given_repository, db)


@router.get(
    "/get_notice_by_id",
    status_code=status.HTTP_200_OK,
    response_model=list[NoticeBase] | None,
)
async def get_notice_by_product(
    product: int,
    given_repository: GivenRepository = Depends(GivenRepository),
    notice_repository: NoticeRepository = Depends(NoticeRepository),
    db: AsyncSession = Depends(get_db),
) -> list[NoticeBase] | None:
    return await get_notice_by_product_service(
        product, given_repository, notice_repository, db
    )


@router.post("/given/", status_code=status.HTTP_201_CREATED, response_model=GivenBase)
async def create_notice_for_product(
    id_customer: int,
    notice: NoticeBase,
    product: int,
    given_repository: GivenRepository = Depends(GivenRepository),
    Give_1_repository: Give_1Repository = Depends(Give_1Repository),
    notice_repository: NoticeRepository = Depends(NoticeRepository),
    db: AsyncSession = Depends(get_db),
) -> GivenBase:
    return await create_notice_for_product_service(
        id_customer,
        notice,
        product,
        given_repository,
        Give_1_repository,
        notice_repository,
        db,
    )


@router.put(
    "/given/{given_id}", status_code=status.HTTP_200_OK, response_model=GivenBase
)
async def update_given(
    given_id: int,
    given: GivenBase,
    given_repository: GivenRepository = Depends(GivenRepository),
    db: AsyncSession = Depends(get_db),
) -> GivenBase:
    return await update_given_service(given_id, given, given_repository, db)
