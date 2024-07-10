from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from .repository import CarryOnRepository
from .schema import CarryOnBase
from common import model_to_dict


async def get_carry_ons_service(
    carry_on_repository: CarryOnRepository, db: AsyncSession
) -> list[CarryOnBase]:
    carry_ons = await carry_on_repository.get_carry_on(db)
    carry_ons_list = [model_to_dict(carry_on) for carry_on in carry_ons]
    return [CarryOnBase(**carry_on_dict) for carry_on_dict in carry_ons_list]


async def get_carry_on_by_id_service(
    carry_on_id: int, carry_on_repository: CarryOnRepository, db: AsyncSession
) -> CarryOnBase | None:
    carry_on = await carry_on_repository.get_carry_by_id(db, carry_on_id)
    if carry_on is None:
        return None
    return CarryOnBase(**model_to_dict(carry_on))


async def create_carry_on_service(
    carry_on: CarryOnBase,
    carry_on_id: int,
    carry_on_repository: CarryOnRepository,
    db: AsyncSession,
) -> CarryOnBase:
    existing_carry_on = await carry_on_repository.get_carry_by_id(db, carry_on_id)
    if existing_carry_on:
        return existing_carry_on
    new_carry_on = await carry_on_repository.create_carry_on(db, carry_on)
    return CarryOnBase(**model_to_dict(new_carry_on))


async def update_carry_on_service(
    carry_on_id: int,
    carry_on: CarryOnBase,
    carry_on_repository: CarryOnRepository,
    db: AsyncSession,
) -> CarryOnBase:
    updated_carry_on = await carry_on_repository.update_carry_on(
        db, carry_on_id, carry_on
    )
    if updated_carry_on is None:
        raise HTTPException(status_code=404, detail="carry_on not found")
    return CarryOnBase(**model_to_dict(updated_carry_on))
