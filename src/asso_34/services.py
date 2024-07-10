from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from .repository import Asso_34Repository
from .schema import Asso_34Base
from common import model_to_dict


async def get_asso_34s_service(
    asso_34_repository: Asso_34Repository, db: AsyncSession
) -> list[Asso_34Base]:
    asso_34s = await asso_34_repository.get_asso_34(db)
    asso_34s_list = [model_to_dict(asso_34) for asso_34 in asso_34s]
    return [Asso_34Base(**asso_34_dict) for asso_34_dict in asso_34s_list]


async def get_asso_34_by_id_service(
    asso_34_id: int, asso_34_repository: Asso_34Repository, db: AsyncSession
) -> Asso_34Base:
    asso_34 = await asso_34_repository.get_asso_34_by_id(db, asso_34_id)
    if asso_34 is None:
        raise HTTPException(status_code=404, detail="asso_34 not found")
    return Asso_34Base(**model_to_dict(asso_34))


async def create_asso_34_service(
    asso_34: Asso_34Base, asso_34_repository: Asso_34Repository, db: AsyncSession
) -> Asso_34Base:
    new_asso_34 = await asso_34_repository.create_asso_34(db, asso_34)
    return Asso_34Base(**model_to_dict(new_asso_34))


async def update_asso_34_service(
    asso_34_id: int,
    asso_34: Asso_34Base,
    asso_34_repository: Asso_34Repository,
    db: AsyncSession,
) -> Asso_34Base:
    updated_asso_34 = await asso_34_repository.update_asso_34(db, asso_34_id, asso_34)
    if updated_asso_34 is None:
        raise HTTPException(status_code=404, detail="asso_34 not found")
    return Asso_34Base(**model_to_dict(updated_asso_34))
