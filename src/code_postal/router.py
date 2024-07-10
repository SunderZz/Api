from .schema import CodePostalBase, CodePostalIdBase
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from .repository import CodePostalRepository
from .services import (
    get_code_postal_service,
    get_code_postal_id_service,
    create_code_postales_service,
    update_code_postal_service,
    get_city_by_code_service
)
from city.schema import CityBase
from city.repository import CityRepository
from got_3.repository import GotRepository

router = APIRouter(tags=["code_postal"])

@router.get("/code_postal/", status_code=status.HTTP_200_OK, response_model=list[CodePostalBase])
async def get_code_postal(
    code_postal_repository: CodePostalRepository = Depends(CodePostalRepository),
    db: AsyncSession = Depends(get_db),
) -> list[CodePostalBase]:
    return await get_code_postal_service(code_postal_repository, db)

@router.get("/code_postal/{code_postal}", response_model=CodePostalIdBase)
async def get_code_postal_id(
    code_postal: int,
    code_postal_repository: CodePostalRepository = Depends(CodePostalRepository),
    db: AsyncSession = Depends(get_db),
) -> CodePostalIdBase:
    return await get_code_postal_id_service(code_postal, code_postal_repository, db)

@router.get("/code_postal_name_by_id/", response_model=CodePostalIdBase)
async def get_code_postal_name(
    code_postal: int,
    code_postal_repository: CodePostalRepository = Depends(CodePostalRepository),
    db: AsyncSession = Depends(get_db),
) -> CodePostalIdBase:
    return await get_code_postal_id_service(code_postal, code_postal_repository, db)

@router.get("/code_postal_informations/", response_model=CodePostalIdBase)
async def get_code_postal_with_id(
    code_postal: int,
    code_postal_repository: CodePostalRepository = Depends(CodePostalRepository),
    db: AsyncSession = Depends(get_db),
) -> CodePostalIdBase:
    return await get_code_postal_id_service(code_postal, code_postal_repository, db)

@router.post("/code_postal/", status_code=status.HTTP_201_CREATED, response_model=CodePostalIdBase)
async def create_code_postales(
    code_postal: CodePostalBase,
    code_postal_repository: CodePostalRepository = Depends(CodePostalRepository),
    db: AsyncSession = Depends(get_db),
) -> CodePostalIdBase:
    return await create_code_postales_service(code_postal, code_postal_repository, db)

@router.put("/code_postal/{code_postal_id}", status_code=status.HTTP_200_OK, response_model=CodePostalIdBase)
async def update_code_postal(
    code_postal_id: int,
    code_postal: CodePostalBase,
    code_postal_repository: CodePostalRepository = Depends(CodePostalRepository),
    db: AsyncSession = Depends(get_db),
) -> CodePostalIdBase:
    return await update_code_postal_service(code_postal_id, code_postal, code_postal_repository, db)

@router.get("/code_postal_city/", response_model=CityBase | list[CityBase])
async def get_city_by_code(
    code_id: int,
    got_repository: GotRepository = Depends(GotRepository),
    city_repository: CityRepository = Depends(CityRepository),
    db: AsyncSession = Depends(get_db),
) -> CityBase | list[CityBase]:
    return await get_city_by_code_service(code_id, got_repository, city_repository, db)
