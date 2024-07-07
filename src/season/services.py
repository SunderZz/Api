from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from .repository import SeasonRepository
from .schema import SeasonBase, SeasonRetrieveBase
from common import model_to_dict

async def get_seasons_service(season_repository: SeasonRepository, db: AsyncSession) -> list[SeasonRetrieveBase]:
    seasons = await season_repository.get_seasons(db)
    season_dict = [model_to_dict(season) for season in seasons]
    return [SeasonRetrieveBase(**dict) for dict in season_dict]

async def create_season_service(season: SeasonBase, season_repository: SeasonRepository, db: AsyncSession) -> SeasonBase:
    new_season = await season_repository.create_season(db, season)
    season_dict = model_to_dict(new_season)
    return SeasonBase(**season_dict)

async def get_season_by_id_service(id: int, season_repository: SeasonRepository, db: AsyncSession) -> SeasonRetrieveBase:
    season = await season_repository.get_season_by_id(db, id)
    if season is None:
        raise HTTPException(status_code=404, detail="Season is not found")
    season_dict = model_to_dict(season)
    return SeasonRetrieveBase(**season_dict)

async def get_season_by_name_service(name: str, season_repository: SeasonRepository, db: AsyncSession) -> SeasonRetrieveBase:
    season = await season_repository.get_season_by_name(db, name)
    if season is None:
        raise HTTPException(status_code=404, detail="Season is not found")
    season_dict = model_to_dict(season)
    return SeasonRetrieveBase(**season_dict)

async def update_season_service(season_id: int, season: SeasonBase, season_repository: SeasonRepository, db: AsyncSession) -> SeasonBase:
    updated_season = await season_repository.update_season(db, season_id, season)
    if updated_season is None:
        raise HTTPException(status_code=404, detail="Season is not found")
    season_dict = model_to_dict(updated_season)
    return SeasonBase(**season_dict)
