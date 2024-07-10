from database import get_db
from .schema import OperateBase
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from .repository import OperateRepository
from .services import (
    get_operates_service,
    get_operate_by_id_service,
    create_operate_service,
)

router = APIRouter(prefix="/operate", tags=["operate"])


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[OperateBase])
async def get_operates(
    operate_repository: OperateRepository = Depends(OperateRepository),
    db: AsyncSession = Depends(get_db),
) -> list[OperateBase]:
    return await get_operates_service(operate_repository, db)


@router.get("/{operate_id}", status_code=status.HTTP_200_OK, response_model=OperateBase)
async def get_operate_by_id(
    operate_id: int,
    operate_repository: OperateRepository = Depends(OperateRepository),
    db: AsyncSession = Depends(get_db),
) -> OperateBase:
    return await get_operate_by_id_service(operate_id, operate_repository, db)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=OperateBase)
async def create_operate(
    operate: OperateBase,
    operate_id: int,
    operate_repository: OperateRepository = Depends(OperateRepository),
    db: AsyncSession = Depends(get_db),
) -> OperateBase:
    return await create_operate_service(operate, operate_id, operate_repository, db)
