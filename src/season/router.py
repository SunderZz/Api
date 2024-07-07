import season.models as models
from database import get_db
from .schema import SeasonBase, SeasonRetrieveBase
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from .repository import SeasonRepository
from .services import (
    get_seasons_service,
    create_season_service,
    get_season_by_id_service,
    get_season_by_name_service,
    update_season_service,
)

router = APIRouter(tags=["season"])


@router.get(
    "/seasons", status_code=status.HTTP_200_OK, response_model=list[SeasonRetrieveBase]
)
async def get_seasons(
    season_repository: SeasonRepository = Depends(SeasonRepository),
    db: AsyncSession = Depends(get_db),
) -> list[SeasonRetrieveBase]:
    return await get_seasons_service(season_repository, db)


@router.post("/season/", status_code=status.HTTP_201_CREATED, response_model=SeasonBase)
async def create_season(
    season: SeasonBase,
    season_repository: SeasonRepository = Depends(SeasonRepository),
    db: AsyncSession = Depends(get_db),
) -> SeasonBase:
    return await create_season_service(season, season_repository, db)


@router.get(
    "/get_seasons_by_id",
    status_code=status.HTTP_200_OK,
    response_model=SeasonRetrieveBase,
)
async def get_seasons_with_id(
    id: int,
    season_repository: SeasonRepository = Depends(SeasonRepository),
    db: AsyncSession = Depends(get_db),
) -> SeasonRetrieveBase:
    return await get_season_by_id_service(id, season_repository, db)


@router.get(
    "/get_seasons_by_name",
    status_code=status.HTTP_200_OK,
    response_model=SeasonRetrieveBase,
)
async def get_seasons_by_name(
    name: str,
    season_repository: SeasonRepository = Depends(SeasonRepository),
    db: AsyncSession = Depends(get_db),
) -> SeasonRetrieveBase:
    return await get_season_by_name_service(name, season_repository, db)


@router.put(
    "/season/{season_id}", status_code=status.HTTP_200_OK, response_model=SeasonBase
)
async def update_season(
    season_id: int,
    season: SeasonBase,
    season_repository: SeasonRepository = Depends(SeasonRepository),
    db: AsyncSession = Depends(get_db),
) -> SeasonBase:
    return await update_season_service(season_id, season, season_repository, db)
