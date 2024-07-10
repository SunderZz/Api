from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from .repository import OperateRepository
from .schema import OperateBase
from common import model_to_dict


async def get_operates_service(
    operate_repository: OperateRepository, db: AsyncSession
) -> list[OperateBase]:
    operates = await operate_repository.get_operate(db)
    operates_list = [model_to_dict(operate) for operate in operates]
    return [OperateBase(**operate_dict) for operate_dict in operates_list]


async def get_operate_by_id_service(
    operate_id: int, operate_repository: OperateRepository, db: AsyncSession
) -> OperateBase:
    operate = await operate_repository.get_operate_by_id(db, operate_id)
    if operate is None:
        raise HTTPException(status_code=404, detail="Operate not found")
    return OperateBase(**model_to_dict(operate))


async def create_operate_service(
    operate: OperateBase,
    operate_id: int,
    operate_repository: OperateRepository,
    db: AsyncSession,
) -> OperateBase:
    existing_operate = await operate_repository.get_operate_by_id(db, operate_id)
    if existing_operate:
        return existing_operate
    new_operate = await operate_repository.create_operate(db, operate)
    return OperateBase(**model_to_dict(new_operate))
