from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from .repository import Give_1Repository
from .schema import Give_1Base
from common import model_to_dict


async def get_Give_1s_service(
    Give_1_repository: Give_1Repository, db: AsyncSession
) -> list[Give_1Base]:
    Give_1s = await Give_1_repository.get_give_1(db)
    Give_1s_list = [model_to_dict(Give_1) for Give_1 in Give_1s]
    return [Give_1Base(**Give_1_dict) for Give_1_dict in Give_1s_list]


async def get_Give_1_by_id_service(
    Give_1_id: int, Give_1_repository: Give_1Repository, db: AsyncSession
) -> Give_1Base:
    Give_1 = await Give_1_repository.get_give_1_by_id(db, Give_1_id)
    if Give_1 is None:
        raise HTTPException(status_code=404, detail="Give_1 not found")
    return Give_1Base(**model_to_dict(Give_1))


async def create_Give_notice_service(
    Give_1: Give_1Base, Give_1_repository: Give_1Repository, db: AsyncSession
) -> Give_1Base:
    new_Give_1 = await Give_1_repository.create_give_1(db, Give_1)
    return Give_1Base(**model_to_dict(new_Give_1))


async def update_Give_1_service(
    Give_1_id: int,
    Give_1: Give_1Base,
    Give_1_repository: Give_1Repository,
    db: AsyncSession,
) -> Give_1Base:
    updated_Give_1 = await Give_1_repository.update_give_1(db, Give_1_id, Give_1)
    if updated_Give_1 is None:
        raise HTTPException(status_code=404, detail="Give_1 not found")
    return Give_1Base(**model_to_dict(updated_Give_1))
