from database import get_db
from .schema import IsOnBase
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from .repository import IsOnRepository
from .services import (
    get_is_ons_service,
    get_is_on_by_id_service,
    get_seasons_with_product_service,
    create_is_on_service,
    update_is_on_service,
    delete_is_on_service,
)
from season.schema import SeasonRetrieveBase
from season.repository import SeasonRepository

router = APIRouter(tags=["is_on"])


@router.get("/is_on/", status_code=status.HTTP_200_OK, response_model=list[IsOnBase])
async def get_is_ons(
    is_on_repository: IsOnRepository = Depends(IsOnRepository),
    db: AsyncSession = Depends(get_db),
) -> list[IsOnBase]:
    return await get_is_ons_service(is_on_repository, db)


@router.get(
    "/is_on_by_id/{is_on_id}",
    status_code=status.HTTP_200_OK,
    response_model=IsOnBase | list[IsOnBase],
)
async def get_is_on_by_id(
    is_on_id: int,
    is_on_repository: IsOnRepository = Depends(IsOnRepository),
    db: AsyncSession = Depends(get_db),
) -> IsOnBase | list[IsOnBase]:
    return await get_is_on_by_id_service(is_on_id, is_on_repository, db)


@router.get(
    "/get_seasons_with_product",
    status_code=status.HTTP_200_OK,
    response_model=SeasonRetrieveBase | list[SeasonRetrieveBase],
)
async def get_seasons_with_product(
    is_on_id: int,
    is_on_repository: IsOnRepository = Depends(IsOnRepository),
    season_repository: SeasonRepository = Depends(SeasonRepository),
    db: AsyncSession = Depends(get_db),
) -> SeasonRetrieveBase | list[SeasonRetrieveBase]:
    return await get_seasons_with_product_service(
        is_on_id, is_on_repository, season_repository, db
    )


@router.post("/is_on/", status_code=status.HTTP_201_CREATED, response_model=IsOnBase)
async def create_is_on(
    is_on: IsOnBase,
    is_on_repository: IsOnRepository = Depends(IsOnRepository),
    db: AsyncSession = Depends(get_db),
) -> IsOnBase:
    return await create_is_on_service(is_on, is_on_repository, db)


@router.put(
    "/is_on/{is_on_id}", status_code=status.HTTP_200_OK, response_model=IsOnBase
)
async def update_is_on(
    is_on_id: int,
    is_on: IsOnBase,
    is_on_repository: IsOnRepository = Depends(IsOnRepository),
    db: AsyncSession = Depends(get_db),
) -> IsOnBase:
    return await update_is_on_service(is_on_id, is_on, is_on_repository, db)


@router.delete("/is_on/{is_on_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_is_on(
    is_on_id: int,
    is_on_repository: IsOnRepository = Depends(IsOnRepository),
    db: AsyncSession = Depends(get_db),
) -> None:
    return await delete_is_on_service(is_on_id, is_on_repository, db)
