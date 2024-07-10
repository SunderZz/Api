from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from .repository import CodePostalRepository
from .schema import CodePostalBase, CodePostalIdBase
from common import model_to_dict
from city.repository import CityRepository
from city.services import get_city_by_id_service, get_cities_service
from got_3.repository import GotRepository
from got_3.services import get_got_by_id_service

async def get_code_postal_service(code_postal_repository: CodePostalRepository, db: AsyncSession) -> list[CodePostalBase]:
    code_postal = await code_postal_repository.get_code_postal(db)
    code_postal_list = [model_to_dict(code) for code in code_postal]
    return [CodePostalBase(**code_postal_dict) for code_postal_dict in code_postal_list]

async def get_code_postal_id_service(code_postal: int, code_postal_repository: CodePostalRepository, db: AsyncSession) -> CodePostalIdBase:
    value = await code_postal_repository.get_code_postal_query(db, code_postal)
    if value is None:
        raise HTTPException(status_code=404, detail="code_postal not found or attribute not found")
    return CodePostalIdBase(**model_to_dict(value))

async def create_code_postales_service(code_postal: CodePostalBase, code_postal_repository: CodePostalRepository, db: AsyncSession) -> CodePostalIdBase:
    existing_code_postal = await code_postal_repository.get_code_postal_query(db, code_postal.code_postal)
    if existing_code_postal:
        return CodePostalIdBase(**model_to_dict(existing_code_postal))
    new_code_postal = await code_postal_repository.create_code_postal(db, code_postal)
    return CodePostalIdBase(**model_to_dict(new_code_postal))

async def update_code_postal_service(code_postal_id: int, code_postal: CodePostalBase, code_postal_repository: CodePostalRepository, db: AsyncSession) -> CodePostalIdBase:
    updated_code_postal = await code_postal_repository.update_code_postal(db, code_postal_id, code_postal)
    if updated_code_postal is None:
        raise HTTPException(status_code=404, detail="code_postal not found")
    return CodePostalIdBase(**model_to_dict(updated_code_postal))

async def get_city_by_code_service(code_id: int, got_repository: GotRepository, city_repository: CityRepository, db: AsyncSession) -> list:
    cities = await get_cities_service(city_repository, db)
    city_in_code_ids = []
    for city in cities:
        got = await get_got_by_id_service(code_id, got_repository, db)
        if isinstance(got, list):
            for code in got:
                if code.Id_City == city.Id_City:
                    city_in_code_ids.append(code.Id_City)
        else:
            if got.Id_City == city.Id_City:
                city_in_code_ids.append(got.Id_City)
    results = []
    for city_id in city_in_code_ids:
        result = await get_city_by_id_service(city_id, city_repository, db)
        results.append(result)
    return results
