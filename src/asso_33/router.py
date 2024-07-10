from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from .schema import Asso_33Base
from .repository import Asso_33Repository
from .services import Asso33Service

router = APIRouter(tags=["asso_33"])


def get_service(
    asso_33_repository: Asso_33Repository = Depends(Asso_33Repository),
) -> Asso33Service:
    return Asso33Service(asso_33_repository)


@router.get(
    "/asso_33/", status_code=status.HTTP_200_OK, response_model=list[Asso_33Base]
)
async def get_asso_33s(
    db: AsyncSession = Depends(get_db), service: Asso33Service = Depends(get_service)
) -> list[Asso_33Base]:
    return await service.get_all_asso_33(db)


@router.get(
    "/asso_33/{asso_33_id}", status_code=status.HTTP_200_OK, response_model=Asso_33Base
)
async def get_asso_33_by_id(
    asso_33_id: int,
    db: AsyncSession = Depends(get_db),
    service: Asso33Service = Depends(get_service),
) -> Asso_33Base:
    return await service.get_asso_33_by_id(db, asso_33_id)


@router.post(
    "/asso_33/", status_code=status.HTTP_201_CREATED, response_model=Asso_33Base
)
async def create_asso_33(
    asso_33: Asso_33Base,
    db: AsyncSession = Depends(get_db),
    service: Asso33Service = Depends(get_service),
) -> Asso_33Base:
    return await service.create_asso_33(db, asso_33)


@router.put(
    "/asso_33/{asso_33_id}", status_code=status.HTTP_200_OK, response_model=Asso_33Base
)
async def update_asso_33(
    asso_33_id: int,
    asso_33: Asso_33Base,
    db: AsyncSession = Depends(get_db),
    service: Asso33Service = Depends(get_service),
) -> Asso_33Base:
    return await service.update_asso_33(db, asso_33_id, asso_33)
