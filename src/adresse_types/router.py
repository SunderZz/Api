from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from .schema import AdresseTypeBase
from .repository import AdresseTypesRepository
from .services import AdresseTypesService

router = APIRouter(tags=["adresse_types"])


def get_service(
    adresse_types_repository: AdresseTypesRepository = Depends(AdresseTypesRepository),
) -> AdresseTypesService:
    return AdresseTypesService(adresse_types_repository)


@router.get(
    "/adresses_types/",
    status_code=status.HTTP_200_OK,
    response_model=list[AdresseTypeBase],
)
async def get_adresses_types(
    db: AsyncSession = Depends(get_db),
    service: AdresseTypesService = Depends(get_service),
) -> list[AdresseTypeBase]:
    return await service.get_all_adresse_types(db)


@router.get("/adresses_types/{adresse_type_id}", response_model=AdresseTypeBase)
async def get_adresse_type_by_id(
    adresse_type_id: str,
    db: AsyncSession = Depends(get_db),
    service: AdresseTypesService = Depends(get_service),
) -> AdresseTypeBase:
    return await service.get_adresse_type_by_id(db, adresse_type_id)


@router.get(
    "/adresses_types_by_user/{user_id}",
    response_model=AdresseTypeBase | list[AdresseTypeBase],
)
async def get_adresse_types_by_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    service: AdresseTypesService = Depends(get_service),
) -> AdresseTypeBase | list[AdresseTypeBase]:
    return await service.get_adresse_types_by_user(db, user_id)


@router.post(
    "/adresses_types/",
    status_code=status.HTTP_201_CREATED,
    response_model=AdresseTypeBase,
)
async def create_adresse_type(
    adresse_type: AdresseTypeBase,
    db: AsyncSession = Depends(get_db),
    service: AdresseTypesService = Depends(get_service),
) -> AdresseTypeBase:
    return await service.create_adresse_type(db, adresse_type)


@router.put(
    "/adresses_types/{adresse_type_id}",
    status_code=status.HTTP_200_OK,
    response_model=AdresseTypeBase,
)
async def update_adresse_type(
    adresse_type_id: int,
    adresse_type: AdresseTypeBase,
    db: AsyncSession = Depends(get_db),
    service: AdresseTypesService = Depends(get_service),
) -> AdresseTypeBase:
    return await service.update_adresse_type(db, adresse_type_id, adresse_type)
