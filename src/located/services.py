from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from .repository import LocatedRepository
from .schema import LocatedBase
from common import model_to_dict


async def get_locateds_service(
    located_repository: LocatedRepository, db: AsyncSession
) -> list[LocatedBase]:
    locateds = await located_repository.get_located(db)
    locateds_list = [model_to_dict(located) for located in locateds]
    return [LocatedBase(**located_dict) for located_dict in locateds_list]


async def get_located_by_ids_service(
    located_id: int, located_repository: LocatedRepository, db: AsyncSession
) -> LocatedBase:
    located = await located_repository.get_located_by_id(db, located_id)
    if located is None:
        raise HTTPException(status_code=404, detail="Located not found")
    return LocatedBase(**model_to_dict(located))


async def create_located_service(
    located: LocatedBase, located_repository: LocatedRepository, db: AsyncSession
) -> LocatedBase:
    id_code = located.Id_Users_adresses
    existing_code_postal = await located_repository.get_located_by_id(db, id_code)
    if existing_code_postal is not None:
        return LocatedBase(**model_to_dict(existing_code_postal))
    new_located = await located_repository.create_located(db, located)
    return LocatedBase(**model_to_dict(new_located))


async def update_located_service(
    located_id: int,
    located: LocatedBase,
    located_repository: LocatedRepository,
    db: AsyncSession,
) -> LocatedBase:
    updated_located = await located_repository.update_located(db, located_id, located)
    if updated_located is None:
        raise HTTPException(status_code=404, detail="Located not found")
    return LocatedBase(**model_to_dict(updated_located))
