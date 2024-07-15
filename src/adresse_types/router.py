from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from .schema import AdresseTypeBase
from .repository import AdresseTypesRepository
from .services import (
    get_adresse_type_by_id_services,
    get_adresse_types_by_user_services,
    get_all_adresse_types_services,
    create_adresse_type_services,
    update_adresse_type_services,
)

router = APIRouter(tags=["adresse_types"])


@router.get(
    "/adresses_types/",
    status_code=status.HTTP_200_OK,
    response_model=list[AdresseTypeBase],
)
async def get_adresses_types(
    db: AsyncSession = Depends(get_db),
    adresse_type_repository: AdresseTypesRepository = Depends(AdresseTypesRepository),
) -> list[AdresseTypeBase]:
    return await get_all_adresse_types_services(db, adresse_type_repository)


@router.get("/adresses_types/{adresse_type_id}", response_model=AdresseTypeBase)
async def get_adresse_type_by_id(
    adresse_type_id: int,
    db: AsyncSession = Depends(get_db),
    adresse_type_repository: AdresseTypesRepository = Depends(AdresseTypesRepository),
) -> AdresseTypeBase:
    return await get_adresse_type_by_id_services(
        db, adresse_type_id, adresse_type_repository
    )


@router.get("/adresses_types_by_user/{user_id}", response_model=AdresseTypeBase | None)
async def get_adresse_types_by_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    adresse_type_repository: AdresseTypesRepository = Depends(AdresseTypesRepository),
) -> AdresseTypeBase | None:
    return await get_adresse_types_by_user_services(
        user_id, db, adresse_type_repository
    )


@router.post(
    "/adresses_types/",
    status_code=status.HTTP_201_CREATED,
    response_model=AdresseTypeBase,
)
async def create_adresse_type(
    adresse_type: AdresseTypeBase,
    adresse_type_repository: AdresseTypesRepository = Depends(AdresseTypesRepository),
    db: AsyncSession = Depends(get_db),
) -> AdresseTypeBase:
    return await create_adresse_type_services(adresse_type, db, adresse_type_repository)


@router.put(
    "/adresses_types/{adresse_type_id}",
    status_code=status.HTTP_200_OK,
    response_model=AdresseTypeBase,
)
async def update_adresse_type(
    adresse_type_id: int,
    adresse_type: AdresseTypeBase,
    db: AsyncSession = Depends(get_db),
    adresse_type_repository: AdresseTypesRepository = Depends(AdresseTypesRepository),
) -> AdresseTypeBase:
    return await update_adresse_type_services(
        db, adresse_type_id, adresse_type_repository, adresse_type
    )
