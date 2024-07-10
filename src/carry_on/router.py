from database import get_db
from .schema import CarryOnBase
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from .repository import CarryOnRepository
from .services import (
    get_carry_ons_service,
    get_carry_on_by_id_service,
    create_carry_on_service,
    update_carry_on_service,
)

router = APIRouter(tags=["carry_on"])


@router.get(
    "/carry_on/", status_code=status.HTTP_200_OK, response_model=list[CarryOnBase]
)
async def get_carry_ons(
    carry_on_repository: CarryOnRepository = Depends(CarryOnRepository),
    db: AsyncSession = Depends(get_db),
) -> list[CarryOnBase]:
    return await get_carry_ons_service(carry_on_repository, db)


@router.get(
    "/carry_on_by_id", status_code=status.HTTP_200_OK, response_model=CarryOnBase | None
)
async def get_carry_onose_by_id(
    carry_on_id: int,
    carry_on_repository: CarryOnRepository = Depends(CarryOnRepository),
    db: AsyncSession = Depends(get_db),
) -> CarryOnBase | None:
    return await get_carry_on_by_id_service(carry_on_id, carry_on_repository, db)


@router.post(
    "/carry_on/", status_code=status.HTTP_201_CREATED, response_model=CarryOnBase
)
async def create_carry_on(
    carry_on: CarryOnBase,
    carry_on_id: int,
    carry_on_repository: CarryOnRepository = Depends(CarryOnRepository),
    db: AsyncSession = Depends(get_db),
) -> CarryOnBase:
    return await create_carry_on_service(carry_on, carry_on_id, carry_on_repository, db)


@router.put(
    "/carry_on/{carry_on_id}",
    status_code=status.HTTP_200_OK,
    response_model=CarryOnBase,
)
async def update_carry_on(
    carry_on_id: int,
    carry_on: CarryOnBase,
    carry_on_repository: CarryOnRepository = Depends(CarryOnRepository),
    db: AsyncSession = Depends(get_db),
) -> CarryOnBase:
    return await update_carry_on_service(carry_on_id, carry_on, carry_on_repository, db)
