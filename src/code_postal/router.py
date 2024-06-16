import users.models as models
from typing import Annotated
from .schema import CodePostalBase,CodePostalIdBase
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from database import engine2, AsyncSessionLocal
from common import model_to_dict
from .repository import CodePostalRepository
from city.schema import CityBase
from city.router import get_city_with_ids,get_cities
from city.repository import CityRepository
from got_3.router import get_got_by_id
from got_3.repository import GotRepository
from got_3.schema import GotBase


router = APIRouter(tags=["code_postal"])


@router.get("/code_postal/", status_code=status.HTTP_200_OK, response_model=list[CodePostalBase])
async def get_code_postal(code_postal_repository: CodePostalRepository = Depends(CodePostalRepository),db:AsyncSession= Depends(get_db))-> list[CodePostalBase]:
    code_postal = await code_postal_repository.get_code_postal(db)
    code_postal_list = [model_to_dict(code) for code in code_postal]
    return [CodePostalBase(**code_postal_dict) for code_postal_dict in code_postal_list]


@router.get("/code_postal/{code_postal}", response_model=CodePostalIdBase)
async def get_code_postal_value(code_postal: int, code_postal_repository: CodePostalRepository = Depends(CodePostalRepository), db:AsyncSession= Depends(get_db)) -> CodePostalIdBase:
    value = await code_postal_repository.get_code_postal_query(db, code_postal)
    if value is None:
        raise HTTPException(status_code=404, detail="code_postal not found or attribute not found")
    code_postal_dict = model_to_dict(value)
        
    return CodePostalIdBase(**code_postal_dict)

@router.get("/code_postal_name_by_id/", response_model=CodePostalIdBase)
async def get_code_postal_name(code_postal: int, code_postal_repository: CodePostalRepository = Depends(CodePostalRepository), db:AsyncSession= Depends(get_db)) -> CodePostalIdBase:
    value = await code_postal_repository.get_code_postal_query(db, code_postal)
    if value is None:
        return None
    code_postal_dict = model_to_dict(value)
        
    return CodePostalIdBase(**code_postal_dict)

@router.get("/code_postal_informations/", response_model=CodePostalIdBase)
async def get_code_postal_with_id(code_postal: int, code_postal_repository: CodePostalRepository = Depends(CodePostalRepository), db:AsyncSession= Depends(get_db)) -> CodePostalIdBase:
    value = await code_postal_repository.get_code_postal_by_id(db, code_postal)
    if value is None:
        return None
    code_postal_dict = model_to_dict(value)
        
    return CodePostalIdBase(**code_postal_dict)


@router.post("/code_postal/", status_code=status.HTTP_201_CREATED, response_model=CodePostalIdBase)
async def create_code_postales(code_postal: CodePostalBase,code_postal_repository: CodePostalRepository = Depends(CodePostalRepository), db:AsyncSession= Depends(get_db))-> CodePostalIdBase:
    existing_code_postal = await get_code_postal_name(code_postal.code_postal,code_postal_repository,db)
    if existing_code_postal:
        return existing_code_postal

    new_code_postal = await code_postal_repository.create_code_postal(db, code_postal)
    code_postal_dict = model_to_dict(new_code_postal)
    return CodePostalIdBase(**code_postal_dict)

@router.put("/code_postal/{code_postal_id}", status_code=status.HTTP_200_OK, response_model=CodePostalIdBase)
async def update_code_postal(code_postal_id: int, code_postal: CodePostalBase,code_postal_repository: CodePostalRepository = Depends(CodePostalRepository), db:AsyncSession= Depends(get_db))-> CodePostalIdBase:
    existing_code_postal = await get_code_postal_name(code_postal.code_postal,code_postal_repository,db)
    if not existing_code_postal:
        code_postal_created = await create_code_postales(code_postal,code_postal_repository, db)
        return code_postal_created
    updated_code_postal = await code_postal_repository.update_code_postal(db, code_postal_id, code_postal)
    code_postal_dict = model_to_dict(updated_code_postal) 
    return CodePostalIdBase(**code_postal_dict)

@router.get("/code_postal_city/", response_model=CityBase |list[CityBase])
async def get_city_by_code(code_id: int, got_repository: GotRepository = Depends(GotRepository),city_repository: CityRepository = Depends(CityRepository), db:AsyncSession= Depends(get_db)) -> CityBase |list[CityBase]:
    city = await get_cities(city_repository, db)
    city_in_code_ids = []
    for cities in city:
        value = await get_got_by_id(code_id,got_repository,db)
        if isinstance(value, list):
            for code in value:
                if code.Id_City == cities.Id_City:
                    city_in_code_ids.append(code.Id_City)
        else:

            if value.Id_City == cities.Id_City:
                city_in_code_ids.append(code.Id_City)
    results = []
    for cities_id in city_in_code_ids:
        result = await get_city_with_ids(cities_id, city_repository, db)
        results.append(result)
    return results
