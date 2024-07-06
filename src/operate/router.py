import operate.models as models
from database import get_db
from typing import Annotated
from .schema import OperateBase
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import engine2, AsyncSessionLocal
from .repository import OperateRepository
from common import model_to_dict


router = APIRouter(prefix="/operate", tags=["operate"])


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[OperateBase])
async def get_operate(
    operate_repository: OperateRepository = Depends(OperateRepository),
    db: AsyncSession = Depends(get_db),
) -> list[OperateBase]:
    operates = await operate_repository.get_operate(db)
    return operates


@router.get(
    "/operate", status_code=status.HTTP_200_OK, response_model=list[OperateBase]
)
async def get_operates(
    operate_repository: OperateRepository = Depends(OperateRepository),
    db: AsyncSession = Depends(get_db),
) -> list[OperateBase]:
    operates = await operate_repository.get_operate(db)
    operates_list = [model_to_dict(operate) for operate in operates]
    return [OperateBase(**operate_dict) for operate_dict in operates_list]


@router.get(
    "/operate/{operate_id}", status_code=status.HTTP_200_OK, response_model=OperateBase
)
async def get_operate_by_id(
    operate_id: int,
    operate_repository: OperateRepository = Depends(OperateRepository),
    db: AsyncSession = Depends(get_db),
) -> OperateBase:
    operate = await operate_repository.get_operate_by_id(db, operate_id)
    if operate is None:
        return None
    return OperateBase(**model_to_dict(operate))


@router.post(
    "/operate/", status_code=status.HTTP_201_CREATED, response_model=OperateBase
)
async def create_operate(
    operate: OperateBase,
    operate_id: int,
    operate_repository: OperateRepository = Depends(OperateRepository),
    db: AsyncSession = Depends(get_db),
) -> OperateBase:
    existing_operate = await operate_repository.get_operate_by_id(db, operate_id)
    if existing_operate:
        return existing_operate
    new_operate = await operate_repository.create_operate(db, operate)
    operate_dict = model_to_dict(new_operate)
    return OperateBase(**operate_dict)


@router.put(
    "/operate/{operate_id}", status_code=status.HTTP_200_OK, response_model=OperateBase
)
async def update_operate(
    operate_id: int,
    operate: OperateBase,
    operate_repository: OperateRepository = Depends(OperateRepository),
    db: AsyncSession = Depends(get_db),
) -> OperateBase:
    updated_operate = await operate_repository.update_operate(db, operate_id, operate)
    if updated_operate is None:
        raise HTTPException(status_code=404, detail="operate not found")
    operate_dict = model_to_dict(updated_operate)
    return OperateBase(**operate_dict)
