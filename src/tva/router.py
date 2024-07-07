import tva.models as models
from .schema import TvaBase, TvaCalculationResult, TvaCreateBase
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from .repository import TvaRepository
from .services import (
    get_tva_service,
    get_tva_with_name_service,
    calculate_tva_service,
    get_all_tva_service,
    update_tva_service,
    create_tva_service,
)

router = APIRouter(tags=["tva"])


@router.get("/tva/{tva_id}", response_model=TvaBase)
async def get_tva(
    tva_id: int,
    tva_repository: TvaRepository = Depends(TvaRepository),
    db: AsyncSession = Depends(get_db),
) -> TvaBase:
    return await get_tva_service(tva_id, tva_repository, db)


@router.get("/tva_name/{tva_name}", response_model=TvaBase)
async def get_tva_with_name(
    tva_name: str,
    tva_repository: TvaRepository = Depends(TvaRepository),
    db: AsyncSession = Depends(get_db),
) -> TvaBase:
    return await get_tva_with_name_service(tva_name, tva_repository, db)


@router.get("/tva/calculate/{tva_name}", response_model=TvaCalculationResult)
async def calculate_tva(
    tva_name: str,
    price: float,
    db: AsyncSession = Depends(get_db),
    tva_repository: TvaRepository = Depends(TvaRepository),
) -> TvaCalculationResult:
    return await calculate_tva_service(tva_name, price, tva_repository, db)


@router.get("/tva", status_code=status.HTTP_200_OK, response_model=list[TvaBase])
async def get_all_tva(
    tva_repository: TvaRepository = Depends(TvaRepository),
    db: AsyncSession = Depends(get_db),
) -> list[TvaBase]:
    return await get_all_tva_service(tva_repository, db)


@router.put("/tva/{tva_id}", response_model=TvaBase)
async def update_tva(
    tva_id: int,
    tva: TvaCreateBase,
    tva_repository: TvaRepository = Depends(TvaRepository),
    db: AsyncSession = Depends(get_db),
) -> TvaBase:
    return await update_tva_service(tva_id, tva, tva_repository, db)


@router.post("/tva/", response_model=TvaBase)
async def create_tva(
    tva: TvaCreateBase,
    tva_repository: TvaRepository = Depends(TvaRepository),
    db: AsyncSession = Depends(get_db),
) -> TvaBase:
    return await create_tva_service(tva, tva_repository, db)
