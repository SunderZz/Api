from database import get_db
from .schema import Asso_34Base
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from .repository import Asso_34Repository
from .services import (
    get_asso_34s_service,
    get_asso_34_by_id_service,
    create_asso_34_service,
    update_asso_34_service,
)

router = APIRouter(tags=["asso_34"])


@router.get(
    "/asso_34/", status_code=status.HTTP_200_OK, response_model=list[Asso_34Base]
)
async def get_asso_34s(
    asso_34_repository: Asso_34Repository = Depends(Asso_34Repository),
    db: AsyncSession = Depends(get_db),
) -> list[Asso_34Base]:
    return await get_asso_34s_service(asso_34_repository, db)


@router.get(
    "/asso_34/{asso_34_id}", status_code=status.HTTP_200_OK, response_model=Asso_34Base
)
async def get_asso_34s_by_id(
    asso_34_id: int,
    asso_34_repository: Asso_34Repository = Depends(Asso_34Repository),
    db: AsyncSession = Depends(get_db),
) -> Asso_34Base:
    return await get_asso_34_by_id_service(asso_34_id, asso_34_repository, db)


@router.post(
    "/asso_34/", status_code=status.HTTP_201_CREATED, response_model=Asso_34Base
)
async def create_asso_34(
    asso_34: Asso_34Base,
    asso_34_repository: Asso_34Repository = Depends(Asso_34Repository),
    db: AsyncSession = Depends(get_db),
) -> Asso_34Base:
    return await create_asso_34_service(asso_34, asso_34_repository, db)


@router.put(
    "/asso_34/{asso_34_id}", status_code=status.HTTP_200_OK, response_model=Asso_34Base
)
async def update_asso_34(
    asso_34_id: int,
    asso_34: Asso_34Base,
    asso_34_repository: Asso_34Repository = Depends(Asso_34Repository),
    db: AsyncSession = Depends(get_db),
) -> Asso_34Base:
    return await update_asso_34_service(asso_34_id, asso_34, asso_34_repository, db)
