from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from .repository import CityRepository
from .schema import CityBase, CityIdBase
from common import model_to_dict


async def get_cities_service(
    city_repository: CityRepository, db: AsyncSession
) -> list[CityIdBase]:
    cities = await city_repository.get_city(db)
    city_list = [model_to_dict(city) for city in cities]
    return [CityIdBase(**city_dict) for city_dict in city_list]


async def get_city_by_name_service(
    city: str, city_repository: CityRepository, db: AsyncSession
) -> CityIdBase:
    value = await city_repository.get_city_by_name(db, city)
    if value is None:
        raise HTTPException(
            status_code=404, detail="city not found or attribute not found"
        )
    return CityIdBase(**model_to_dict(value))


async def get_city_by_id_service(
    city: int, city_repository: CityRepository, db: AsyncSession
) -> CityBase:
    value = await city_repository.get_city_by_id(db, city)
    if value is None:
        raise HTTPException(
            status_code=404, detail="city not found or attribute not found"
        )
    return CityBase(**model_to_dict(value))


async def create_city_service(
    city: CityBase, city_repository: CityRepository, db: AsyncSession
) -> CityIdBase:
    existing_city = await city_repository.get_city_by_name(db, city.Name)
    if existing_city:
        return CityIdBase(**model_to_dict(existing_city))

    new_city = await city_repository.create_city(db, city)
    return CityIdBase(**model_to_dict(new_city))


async def update_city_service(
    city_id: int, city: CityBase, city_repository: CityRepository, db: AsyncSession
) -> CityBase:
    updated_city = await city_repository.update_city(db, city_id, city)
    if updated_city is None:
        raise HTTPException(status_code=404, detail="city not found")
    return CityBase(**model_to_dict(updated_city))
