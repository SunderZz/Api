from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from .repository import ChooseRepository
from .schema import ChooseBase
from common import model_to_dict


async def get_chooses_service(
    choose_repository: ChooseRepository, db: AsyncSession
) -> list[ChooseBase]:
    chooses = await choose_repository.get_choose(db)
    chooses_list = [model_to_dict(choose) for choose in chooses]
    return [ChooseBase(**choose_dict) for choose_dict in chooses_list]


async def get_choose_by_id_service(
    choose_id: int, choose_repository: ChooseRepository, db: AsyncSession
) -> ChooseBase:
    choose = await choose_repository.get_choose_by_id(db, choose_id)
    if choose is None:
        raise HTTPException(status_code=404, detail="choose not found")
    return ChooseBase(**model_to_dict(choose))


async def create_choose_service(
    choose: ChooseBase, choose_repository: ChooseRepository, db: AsyncSession
) -> ChooseBase:
    new_choose = await choose_repository.create_choose(db, choose)
    return ChooseBase(**model_to_dict(new_choose))


async def update_choose_service(
    choose_id: int,
    choose: ChooseBase,
    choose_repository: ChooseRepository,
    db: AsyncSession,
) -> ChooseBase:
    updated_choose = await choose_repository.update_choose(db, choose_id, choose)
    if updated_choose is None:
        raise HTTPException(status_code=404, detail="choose not found")
    return ChooseBase(**model_to_dict(updated_choose))
