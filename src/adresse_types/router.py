import users.models as models
from typing import Annotated
from .schema import AdresseTypeBase
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from database import engine2, AsyncSessionLocal
from common import model_to_dict
from .repository import AdresseTypesRepository


router = APIRouter(tags=["adresse_types"])


@router.get(
    "/adresses_types/",
    status_code=status.HTTP_200_OK,
    response_model=list[AdresseTypeBase],
)
async def get_adresses_types(
    adresses_types_repository: AdresseTypesRepository = Depends(AdresseTypesRepository),
    db: AsyncSession = Depends(get_db),
) -> list[AdresseTypeBase]:
    adresses_types = await adresses_types_repository.get_adressestypes(db)
    adresses_types_list = [
        model_to_dict(adresses_type) for adresses_type in adresses_types
    ]
    return [
        AdresseTypeBase(**adresses_type_dict)
        for adresses_type_dict in adresses_types_list
    ]


@router.get("/adresses_types/{adresses_types}", response_model=AdresseTypeBase)
async def get_adresses_type_value(
    adresses_types: str,
    adresses_types_repository: AdresseTypesRepository = Depends(AdresseTypesRepository),
    db: AsyncSession = Depends(get_db),
) -> AdresseTypeBase:
    value = await adresses_types_repository.get_adressestypes_query(db, adresses_types)
    if value is None:
        raise HTTPException(
            status_code=404, detail="adresses_type not found or attribute not found"
        )
    adresses_type_dict = model_to_dict(value)

    return AdresseTypeBase(**adresses_type_dict)


@router.get(
    "/adresses_types_by_user/{user_id}",
    response_model=AdresseTypeBase | list[AdresseTypeBase],
)
async def get_adresses_type_user(
    user_id: int,
    adresses_types_repository: AdresseTypesRepository = Depends(AdresseTypesRepository),
    db: AsyncSession = Depends(get_db),
) -> AdresseTypeBase | list[AdresseTypeBase]:
    value = await adresses_types_repository.get_adressestypes_user(db, user_id)
    if value is None:
        raise HTTPException(
            status_code=404, detail="adresses_type not found or attribute not found"
        )
    if isinstance(value, list):
        adresses_types_list = [model_to_dict(adresses_type) for adresses_type in value]
        return [
            AdresseTypeBase(**adresses_type_dict)
            for adresses_type_dict in adresses_types_list
        ]
    adresses_type_dict = model_to_dict(value)
    return AdresseTypeBase(**adresses_type_dict)


@router.post(
    "/adresses_types/",
    status_code=status.HTTP_201_CREATED,
    response_model=AdresseTypeBase,
)
async def create_adresses_types(
    adresse_type: AdresseTypeBase,
    adresses_types_repository: AdresseTypesRepository = Depends(AdresseTypesRepository),
    db: AsyncSession = Depends(get_db),
) -> AdresseTypeBase:
    new_adresse_type = await adresses_types_repository.create_adressestypes(
        db, adresse_type
    )
    adresses_type_dict = model_to_dict(new_adresse_type)
    return AdresseTypeBase(**adresses_type_dict)


@router.put(
    "/adresses_types/{adresses_type_id}",
    status_code=status.HTTP_200_OK,
    response_model=AdresseTypeBase,
)
async def update_adresse_type(
    adresses_type_id: int,
    adresse_type: AdresseTypeBase,
    adresses_type_repository: AdresseTypesRepository = Depends(AdresseTypesRepository),
    db: AsyncSession = Depends(get_db),
) -> AdresseTypeBase:
    updated_adresse_type = await adresses_type_repository.update_adressestypes(
        db, adresses_type_id, adresse_type
    )
    if updated_adresse_type is None:
        raise HTTPException(status_code=404, detail="produit_image not found")
    produit_image_dict = model_to_dict(updated_adresse_type)
    return AdresseTypeBase(**produit_image_dict)
