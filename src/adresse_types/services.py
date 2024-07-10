from sqlalchemy.ext.asyncio import AsyncSession
from .schema import AdresseTypeBase
from .repository import AdresseTypesRepository
from common import model_to_dict
from fastapi import HTTPException


class AdresseTypesService:
    def __init__(self, adresse_types_repository: AdresseTypesRepository):
        self.adresse_types_repository = adresse_types_repository

    async def get_all_adresse_types(self, db: AsyncSession) -> list[AdresseTypeBase]:
        adresse_types = await self.adresse_types_repository.get_adressestypes(db)
        return [
            AdresseTypeBase(**model_to_dict(adresse_type))
            for adresse_type in adresse_types
        ]

    async def get_adresse_type_by_id(
        self, db: AsyncSession, adresse_type_id: str
    ) -> AdresseTypeBase:
        adresse_type = await self.adresse_types_repository.get_adressestypes_query(
            db, adresse_type_id
        )
        if not adresse_type:
            raise HTTPException(status_code=404, detail="AdresseType not found")
        return AdresseTypeBase(**model_to_dict(adresse_type))

    async def get_adresse_types_by_user(
        self, db: AsyncSession, user_id: int
    ) -> AdresseTypeBase | list[AdresseTypeBase]:
        adresse_types = await self.adresse_types_repository.get_adressestypes_user(
            db, user_id
        )
        if not adresse_types:
            raise HTTPException(status_code=404, detail="AdresseType not found")
        if isinstance(adresse_types, list):
            return [
                AdresseTypeBase(**model_to_dict(adresse_type))
                for adresse_type in adresse_types
            ]
        return AdresseTypeBase(**model_to_dict(adresse_types))

    async def create_adresse_type(
        self, db: AsyncSession, adresse_type: AdresseTypeBase
    ) -> AdresseTypeBase:
        new_adresse_type = await self.adresse_types_repository.create_adressestypes(
            db, adresse_type
        )
        return AdresseTypeBase(**model_to_dict(new_adresse_type))

    async def update_adresse_type(
        self, db: AsyncSession, adresse_type_id: int, adresse_type: AdresseTypeBase
    ) -> AdresseTypeBase:
        updated_adresse_type = await self.adresse_types_repository.update_adressestypes(
            db, adresse_type_id, adresse_type
        )
        if not updated_adresse_type:
            raise HTTPException(status_code=404, detail="AdresseType not found")
        return AdresseTypeBase(**model_to_dict(updated_adresse_type))
