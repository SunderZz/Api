import season.models as models
from database import get_db
from typing import Annotated
from .schema import SeasonBase, SeasonRetrieveBase
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import engine2, AsyncSessionLocal
from .repository import SeasonRepository
from common import model_to_dict

router = APIRouter(tags=["season"])


@router.get(
    "/seasons", status_code=status.HTTP_200_OK, response_model=list[SeasonRetrieveBase]
)
async def get_seasons(
    season_repository: SeasonRepository = Depends(SeasonRepository),
    db: AsyncSession = Depends(get_db),
) -> list[SeasonRetrieveBase]:
    seasons = await season_repository.get_seasons(db)
    season_dict = [model_to_dict(season) for season in seasons]
    return [SeasonRetrieveBase(**dict) for dict in season_dict]


@router.post("/season/", status_code=status.HTTP_201_CREATED, response_model=SeasonBase)
async def create_season(
    season: SeasonBase,
    season_repository: SeasonRepository = Depends(SeasonRepository),
    db: AsyncSession = Depends(get_db),
) -> SeasonBase:
    new_season = await season_repository.create_season(db, season)
    season_dict = model_to_dict(new_season)
    return SeasonBase(**season_dict)


@router.get(
    "/get_seasons_by_id",
    status_code=status.HTTP_200_OK,
    response_model=SeasonRetrieveBase,
)
async def get_seasons_with_product_id(
    id: int,
    season_repository: SeasonRepository = Depends(SeasonRepository),
    db: AsyncSession = Depends(get_db),
) -> SeasonRetrieveBase:
    season = await season_repository.get_season_by_id(db, id)
    if season is None:
        raise HTTPException(status_code=404, detail="is_on not found")
    season_dict = model_to_dict(season)
    return season_dict


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
    season = await season_repository.get_season_by_name(db, name)
    if season is None:
        raise HTTPException(status_code=404, detail="is_on not found")
    season_dict = model_to_dict(season)
    return season_dict


@router.put(
    "/season/{season_id}", status_code=status.HTTP_200_OK, response_model=SeasonBase
)
async def update_season(
    season_id: int,
    season: SeasonBase,
    season_repository: SeasonRepository = Depends(SeasonRepository),
    db: AsyncSession = Depends(get_db),
) -> SeasonBase:
    updated_season = await season_repository.update_season(db, season_id, season)
    if updated_season is None:
        raise HTTPException(status_code=404, detail="season not found")
    season_dict = model_to_dict(updated_season)
    return SeasonBase(**season_dict)
