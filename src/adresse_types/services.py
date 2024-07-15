from sqlalchemy.ext.asyncio import AsyncSession
from .schema import AdresseTypeBase
from .repository import AdresseTypesRepository
from common import model_to_dict
from fastapi import Depends, HTTPException


async def get_all_adresse_types_services(
    db: AsyncSession,
    adresse_types_repository: AdresseTypesRepository = Depends(AdresseTypesRepository),
) -> list[AdresseTypeBase]:
    adresse_types = await adresse_types_repository.get_adressestypes(db)
    return [
        AdresseTypeBase(**model_to_dict(adresse_type)) for adresse_type in adresse_types
    ]


async def get_adresse_type_by_id_services(
    db: AsyncSession,
    adresse_type_id: int,
    adresse_types_repository: AdresseTypesRepository = Depends(AdresseTypesRepository),
) -> AdresseTypeBase:
    adresse_type = await adresse_types_repository.get_adressestypes_query(
        db, adresse_type_id
    )
    if not adresse_type:
        raise HTTPException(status_code=404, detail="AdresseType not found")
    return AdresseTypeBase(**model_to_dict(adresse_type))


async def get_adresse_types_by_user_services(
    user_id: int, db: AsyncSession, adresse_types_repository: AdresseTypesRepository
) -> AdresseTypeBase | None:
    adresse_types = await adresse_types_repository.get_adressestypes_user(db, user_id)
    if not adresse_types:
        return None

    return AdresseTypeBase(**model_to_dict(adresse_types))


async def create_adresse_type_services(
    adresse_type: AdresseTypeBase,
    db: AsyncSession,
    adresse_types_repository: AdresseTypesRepository = Depends(AdresseTypesRepository),
) -> AdresseTypeBase:
    new_adresse_type = await adresse_types_repository.create_adressestypes(
        db, adresse_type
    )
    return AdresseTypeBase(**model_to_dict(new_adresse_type))


async def update_adresse_type_services(
    db: AsyncSession,
    adresse_type_id: int,
    adresse_type: AdresseTypeBase,
    adresse_types_repository: AdresseTypesRepository = Depends(AdresseTypesRepository),
) -> AdresseTypeBase:
    updated_adresse_type = await adresse_types_repository.update_adressestypes(
        db, adresse_type_id, adresse_type
    )
    if not updated_adresse_type:
        raise HTTPException(status_code=404, detail="AdresseType not found")
    return AdresseTypeBase(**model_to_dict(updated_adresse_type))
