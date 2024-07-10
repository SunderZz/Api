from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from .repository import GiveRepository
from .schema import GiveBase, GiveCalcBase
from common import model_to_dict


async def get_gives_service(
    give_repository: GiveRepository, db: AsyncSession
) -> list[GiveBase]:
    gives = await give_repository.get_give(db)
    gives_list = [model_to_dict(give) for give in gives]
    return [GiveBase(**give_dict) for give_dict in gives_list]


async def get_give_by_id_service(
    give_id: int, give_repository: GiveRepository, db: AsyncSession
) -> GiveBase:
    give = await give_repository.get_give_by_id(db, give_id)
    if give is None:
        raise HTTPException(status_code=404, detail="give not found")
    return GiveBase(**model_to_dict(give))


async def get_give_by_id_producers_service(
    give_id: int, give_repository: GiveRepository, db: AsyncSession
) -> list[GiveBase]:
    gives = await give_repository.get_give_by_id_producers(db, give_id)
    if gives is None:
        raise HTTPException(status_code=404, detail="give not found")
    gives_list = [model_to_dict(give) for give in gives]
    return [GiveBase(**give_dict) for give_dict in gives_list]


async def create_give_service(
    give: GiveBase, give_repository: GiveRepository, db: AsyncSession
) -> GiveBase:
    new_give = await give_repository.create_give(db, give)
    return GiveBase(**model_to_dict(new_give))


async def update_give_service(
    give_id: int, give: GiveCalcBase, give_repository: GiveRepository, db: AsyncSession
) -> GiveBase:
    updated_give = await give_repository.update_give(db, give_id, give)
    if updated_give is None:
        raise HTTPException(status_code=404, detail="give not found")
    return GiveBase(**model_to_dict(updated_give))
