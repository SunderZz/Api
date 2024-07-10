from .schema import CityBase, CityIdBase
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from .repository import CityRepository
from .services import (
    get_cities_service,
    get_city_by_name_service,
    get_city_by_id_service,
    create_city_service,
    update_city_service
)

router = APIRouter(tags=["city"])

@router.get("/all_city/", status_code=status.HTTP_200_OK, response_model=list[CityIdBase])
async def get_cities(
    city_repository: CityRepository = Depends(CityRepository),
    db: AsyncSession = Depends(get_db),
) -> list[CityIdBase]:
    return await get_cities_service(city_repository, db)

@router.get("/city_by_name/", response_model=CityIdBase)
async def get_city_by_names(
    city: str,
    city_repository: CityRepository = Depends(CityRepository),
    db: AsyncSession = Depends(get_db),
) -> CityIdBase:
    return await get_city_by_name_service(city, city_repository, db)

@router.get("/city_with_id/", response_model=CityBase)
async def get_city_with_ids(
    city: int,
    city_repository: CityRepository = Depends(CityRepository),
    db: AsyncSession = Depends(get_db),
) -> CityBase:
    return await get_city_by_id_service(city, city_repository, db)

@router.post("/city/", status_code=status.HTTP_201_CREATED, response_model=CityIdBase)
async def create_city(
    city: CityBase,
    city_repository: CityRepository = Depends(CityRepository),
    db: AsyncSession = Depends(get_db),
) -> CityIdBase:
    return await create_city_service(city, city_repository, db)

@router.put("/city/{city_id}", status_code=status.HTTP_200_OK, response_model=CityBase)
async def update_city(
    city_id: int,
    city: CityBase,
    city_repository: CityRepository = Depends(CityRepository),
    db: AsyncSession = Depends(get_db),
) -> CityBase:
    return await update_city_service(city_id, city, city_repository, db)
