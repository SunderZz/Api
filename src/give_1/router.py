from database import get_db
from .schema import Give_1Base
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from .repository import Give_1Repository
from .services import (
    get_Give_1s_service,
    get_Give_1_by_id_service,
    create_Give_notice_service,
    update_Give_1_service,
)

router = APIRouter(tags=["give_1"])


@router.get("/Give_1/", status_code=status.HTTP_200_OK, response_model=list[Give_1Base])
async def get_Give_1s(
    Give_1_repository: Give_1Repository = Depends(Give_1Repository),
    db: AsyncSession = Depends(get_db),
) -> list[Give_1Base]:
    return await get_Give_1s_service(Give_1_repository, db)


@router.get(
    "/Give_1/{Give_1_id}", status_code=status.HTTP_200_OK, response_model=Give_1Base
)
async def get_Give_1_by_id(
    Give_1_id: int,
    Give_1_repository: Give_1Repository = Depends(Give_1Repository),
    db: AsyncSession = Depends(get_db),
) -> Give_1Base:
    return await get_Give_1_by_id_service(Give_1_id, Give_1_repository, db)


@router.post("/Give_1/", status_code=status.HTTP_201_CREATED, response_model=Give_1Base)
async def create_Give_notice(
    Give_1: Give_1Base,
    Give_1_repository: Give_1Repository = Depends(Give_1Repository),
    db: AsyncSession = Depends(get_db),
) -> Give_1Base:
    return await create_Give_notice_service(Give_1, Give_1_repository, db)


@router.put(
    "/Give_1/{Give_1_id}", status_code=status.HTTP_200_OK, response_model=Give_1Base
)
async def update_Give_1(
    Give_1_id: int,
    Give_1: Give_1Base,
    Give_1_repository: Give_1Repository = Depends(Give_1Repository),
    db: AsyncSession = Depends(get_db),
) -> Give_1Base:
    return await update_Give_1_service(Give_1_id, Give_1, Give_1_repository, db)
