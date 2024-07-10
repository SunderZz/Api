from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from .repository import IsOnRepository
from .schema import IsOnBase
from common import model_to_dict
from season.repository import SeasonRepository
from season.router import get_seasons_with_id
from season.schema import SeasonRetrieveBase


async def get_is_ons_service(
    is_on_repository: IsOnRepository, db: AsyncSession
) -> list[IsOnBase]:
    is_ons = await is_on_repository.get_is_on(db)
    is_ons_list = [model_to_dict(is_on) for is_on in is_ons]
    return [IsOnBase(**is_on_dict) for is_on_dict in is_ons_list]


async def get_is_on_by_id_service(
    is_on_id: int, is_on_repository: IsOnRepository, db: AsyncSession
) -> IsOnBase | list[IsOnBase]:
    is_on = await is_on_repository.get_is_on_by_id(db, is_on_id)
    if is_on is None:
        raise HTTPException(status_code=404, detail="is_on not found")
    if isinstance(is_on, list):
        is_ons_list = [model_to_dict(is_ons) for is_ons in is_on]
        return [IsOnBase(**is_on_dict) for is_on_dict in is_ons_list]
    else:
        return IsOnBase(**model_to_dict(is_on))


async def get_seasons_with_product_service(
    is_on_id: int,
    is_on_repository: IsOnRepository,
    season_repository: SeasonRepository,
    db: AsyncSession,
) -> SeasonRetrieveBase | list[SeasonRetrieveBase]:
    is_on = await is_on_repository.get_season_with_produt(db, is_on_id)
    if is_on is None:
        raise HTTPException(status_code=404, detail="is_on not found")
    if isinstance(is_on, list):
        all_season = []
        is_ons_dict = [model_to_dict(is_ons) for is_ons in is_on]
        result = [IsOnBase(**dict) for dict in is_ons_dict]
        for season in result:
            id_season = season.Id_Season
            seasons = await get_seasons_with_id(id_season, season_repository, db)
            all_season.append(seasons)
        return all_season
    else:
        result = IsOnBase(**model_to_dict(is_on))
        id_season = result.Id_Season
        seasons = await get_seasons_with_id(id_season, season_repository, db)
        return seasons


async def create_is_on_service(
    is_on: IsOnBase, is_on_repository: IsOnRepository, db: AsyncSession
) -> IsOnBase:
    new_is_on = await is_on_repository.create_is_on(db, is_on)
    return IsOnBase(**model_to_dict(new_is_on))


async def update_is_on_service(
    is_on_id: int, is_on: IsOnBase, is_on_repository: IsOnRepository, db: AsyncSession
) -> IsOnBase:
    updated_is_on = await is_on_repository.update_is_on(db, is_on_id, is_on)
    if updated_is_on is None:
        raise HTTPException(status_code=404, detail="is_on not found")
    return IsOnBase(**model_to_dict(updated_is_on))


async def delete_is_on_service(
    is_on_id: int, is_on_repository: IsOnRepository, db: AsyncSession
) -> None:
    deleted_is_on = await is_on_repository.delete_is_on(db, is_on_id)
    if deleted_is_on is None:
        raise HTTPException(status_code=404, detail="is_on not found")
