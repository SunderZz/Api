import users.models as models
from typing import Annotated
from .schema import CityBase, CityIdBase
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from database import engine2, AsyncSessionLocal
from common import model_to_dict
from .repository import CityRepository

router = APIRouter(tags=["city"])


@router.get(
    "/all_city/", status_code=status.HTTP_200_OK, response_model=list[CityIdBase]
)
async def get_cities(
    city_repository: CityRepository = Depends(CityRepository),
    db: AsyncSession = Depends(get_db),
) -> list[CityIdBase]:
    cities = await city_repository.get_city(db)
    city_list = [model_to_dict(city) for city in cities]
    return [CityIdBase(**city_dict) for city_dict in city_list]


@router.get(
    "/city_id/", status_code=status.HTTP_200_OK, response_model=list[CityIdBase]
)
async def get_city_id(
    city_repository: CityRepository = Depends(CityRepository),
    db: AsyncSession = Depends(get_db),
) -> list[CityIdBase]:
    cities = await city_repository.get_city(db)
    city_list = [model_to_dict(city) for city in cities]
    return [CityIdBase(**city_dict) for city_dict in city_list]


@router.get("/city_by_name/", response_model=CityIdBase)
async def get_city_by_names(
    city: str,
    city_repository: CityRepository = Depends(CityRepository),
    db: AsyncSession = Depends(get_db),
) -> CityIdBase:
    value = await city_repository.get_city_by_name(db, city)
    if value is None:
        raise HTTPException(
            status_code=404, detail="city not found or attribute not found"
        )
    city_dict = model_to_dict(value)

    return CityIdBase(**city_dict)


@router.get("/city_with_id/", response_model=CityBase)
async def get_city_with_ids(
    city: int,
    city_repository: CityRepository = Depends(CityRepository),
    db: AsyncSession = Depends(get_db),
) -> CityBase:
    value = await city_repository.get_city_by_id(db, city)
    if value is None:
        raise HTTPException(
            status_code=404, detail="city not found or attribute not found"
        )
    if isinstance(value, list):
        city_list = [model_to_dict(city) for city in value]
        return [CityBase(**city_dict) for city_dict in city_list]
    city_dict = model_to_dict(value)
    return CityBase(**city_dict)


@router.post("/city/", status_code=status.HTTP_201_CREATED, response_model=CityIdBase)
async def create_city(
    city: CityBase,
    city_repository: CityRepository = Depends(CityRepository),
    db: AsyncSession = Depends(get_db),
) -> CityIdBase:
    existing_city = await city_repository.get_city_by_name(db, city.Name)
    if existing_city:
        city_dict = model_to_dict(existing_city)
        return CityIdBase(**city_dict)

    new_city = await city_repository.create_city(db, city)
    city_dict = model_to_dict(new_city)
    return CityIdBase(**city_dict)


@router.put("/city/{city_id}", status_code=status.HTTP_200_OK, response_model=CityBase)
async def update_city(
    city_id: int,
    city: CityBase,
    city_repository: CityRepository = Depends(CityRepository),
    db: AsyncSession = Depends(get_db),
) -> CityBase:
    updated_city = await city_repository.update_city(db, city_id, city)
    if updated_city is None:
        raise HTTPException(status_code=404, detail="city not found")
    city_dict = model_to_dict(updated_city)
    return CityBase(**city_dict)
