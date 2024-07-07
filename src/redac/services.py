from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from .repository import RedactRepository
from .schema import RedactBase
from common import model_to_dict


async def get_redacts_service(
    redact_repository: RedactRepository, db: AsyncSession
) -> list[RedactBase]:
    redacts = await redact_repository.get_Redact(db)
    redacts_list = [model_to_dict(redact) for redact in redacts]
    return [RedactBase(**redact_dict) for redact_dict in redacts_list]


async def get_redact_value_service(
    admin_id: int, redact_id: int, redact_repository: RedactRepository, db: AsyncSession
) -> RedactBase:
    value = await redact_repository.get_Redact_by_admin_and_recipe(
        db, admin_id, redact_id
    )
    if value is None:
        raise HTTPException(status_code=404, detail="redact not found")
    redact_dict = model_to_dict(value)
    return RedactBase(**redact_dict)


async def create_redact_service(
    admin_id: int,
    redact_id: int,
    redact: RedactBase,
    redact_repository: RedactRepository,
    db: AsyncSession,
) -> RedactBase:
    existing_redac = await redact_repository.get_Redact_by_admin_and_recipe(
        db, admin_id, redact_id
    )
    if existing_redac:
        return existing_redac
    new_redact = await redact_repository.create_Redact(db, redact)
    redact_dict = model_to_dict(new_redact)
    return RedactBase(**redact_dict)


async def update_redact_service(
    admin_id: int,
    recipe_id: int,
    redact: RedactBase,
    redact_repository: RedactRepository,
    db: AsyncSession,
) -> RedactBase:
    updated_redact = await redact_repository.update_Redact(
        db, admin_id, recipe_id, redact
    )
    if updated_redact is None:
        raise HTTPException(status_code=404, detail="redact not found")
    redact_dict = model_to_dict(updated_redact)
    return RedactBase(**redact_dict)
