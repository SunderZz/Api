from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from .repository import TvaRepository
from .schema import TvaBase, TvaCalculationResult, TvaCreateBase
from common import model_to_dict


async def get_tva_service(
    tva_id: int, tva_repository: TvaRepository, db: AsyncSession
) -> TvaBase:
    tva = await tva_repository.get_tva(db, tva_id)
    if tva is None:
        raise HTTPException(status_code=404, detail="Tva not found")
    tva_dict = model_to_dict(tva)
    return TvaBase(**tva_dict)


async def get_tva_with_name_service(
    tva_name: str, tva_repository: TvaRepository, db: AsyncSession
) -> TvaBase:
    tva = await tva_repository.get_tva_by_name(db, tva_name)
    if tva is None:
        raise HTTPException(status_code=404, detail="Tva not found")
    tva_dict = model_to_dict(tva)
    return TvaBase(**tva_dict)


async def calculate_tva_service(
    tva_name: str, price: float, tva_repository: TvaRepository, db: AsyncSession
) -> TvaCalculationResult:
    tva_value = await tva_repository.calculate_tva(db, price, tva_name)
    if tva_value is None:
        raise HTTPException(status_code=404, detail="Tva not found")
    return TvaCalculationResult(value=tva_value)


async def get_all_tva_service(
    tva_repository: TvaRepository, db: AsyncSession
) -> list[TvaBase]:
    Tva = await tva_repository.get_all_tva(db)
    tvas_list = [model_to_dict(tvas) for tvas in Tva]
    return [TvaBase(**tva_dict) for tva_dict in tvas_list]


async def update_tva_service(
    tva_id: int, tva: TvaBase, tva_repository: TvaRepository, db: AsyncSession
) -> TvaBase:
    updated_tva = await tva_repository.update_tva(db, tva, tva_id)
    if updated_tva is None:
        raise HTTPException(status_code=404, detail="Tva not found")
    tva_dict = model_to_dict(updated_tva)
    return TvaBase(**tva_dict)


async def create_tva_service(
    tva: TvaCreateBase, tva_repository: TvaRepository, db: AsyncSession
) -> TvaBase:
    created_tva = await tva_repository.create_tva(db, tva)
    tva_dict = model_to_dict(created_tva)
    return TvaBase(**tva_dict)
