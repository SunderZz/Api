from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from .repository import ManageRepository
from .schema import ManageBase
from common import model_to_dict


async def get_manages_service(
    manage_repository: ManageRepository, db: AsyncSession
) -> list[ManageBase]:
    manages = await manage_repository.get_manage(db)
    manages_list = [model_to_dict(manage) for manage in manages]
    return [ManageBase(**manage_dict) for manage_dict in manages_list]


async def get_manage_by_id_service(
    manage_id: int, manage_repository: ManageRepository, db: AsyncSession
) -> ManageBase:
    manage = await manage_repository.get_manage_by_id(db, manage_id)
    if manage is None:
        raise HTTPException(status_code=404, detail="Manage not found")
    return ManageBase(**model_to_dict(manage))


async def create_manage_service(
    manage: ManageBase,
    manage_id: int,
    manage_repository: ManageRepository,
    db: AsyncSession,
) -> ManageBase:
    existing_manage = await manage_repository.get_manage_by_id(db, manage_id)
    if existing_manage:
        return existing_manage
    new_manage = await manage_repository.create_manage(db, manage)
    return ManageBase(**model_to_dict(new_manage))
