import season.models as models
from database import get_db
from typing import Annotated
from .schema import IsOnBase
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import engine2, AsyncSessionLocal
from .repository import IsOnRepository
from common import model_to_dict
from season.schema import SeasonRetrieveBase
from season.router import get_seasons_with_id
from season.repository import SeasonRepository


router = APIRouter(tags=["is_on"])


@router.get("/is_on/", status_code=status.HTTP_200_OK, response_model=list[IsOnBase])
async def get_is_ons(
    is_on_repository: IsOnRepository = Depends(IsOnRepository),
    db: AsyncSession = Depends(get_db),
) -> list[IsOnBase]:
    is_ons = await is_on_repository.get_is_on(db)
    is_ons_list = [model_to_dict(is_on) for is_on in is_ons]
    return [IsOnBase(**is_on_dict) for is_on_dict in is_ons_list]


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
    is_on = await is_on_repository.get_is_on_by_id(db, is_on_id)
    if is_on is None:
        raise HTTPException(status_code=404, detail="is_on not found")
    if isinstance(is_on, list):
        is_ons_list = [model_to_dict(is_ons) for is_ons in is_on]
        return [IsOnBase(**is_on_dict) for is_on_dict in is_ons_list]
    else:
        return IsOnBase(**model_to_dict(is_on))


@router.get(
    "/get_seasons_with_product",
    status_code=status.HTTP_200_OK,
    response_model=SeasonRetrieveBase,
)
async def get_seasons_with_product(
    is_on_id: int,
    is_on_repository: IsOnRepository = Depends(IsOnRepository),
    season_repository: SeasonRepository = Depends(SeasonRepository),
    db: AsyncSession = Depends(get_db),
) -> SeasonRetrieveBase:
    is_on = await is_on_repository.get_season_with_produt(db, is_on_id)
    if is_on is None:
        raise HTTPException(status_code=404, detail="is_on not found")
    result = IsOnBase(**model_to_dict(is_on))
    id_season = result.Id_Season
    season = await get_seasons_with_product_id(id_season, season_repository, db)
    return season


@router.post("/is_on/", status_code=status.HTTP_201_CREATED, response_model=IsOnBase)
async def create_is_on(
    is_on: IsOnBase,
    is_on_repository: IsOnRepository = Depends(IsOnRepository),
    db: AsyncSession = Depends(get_db),
) -> IsOnBase:
    new_is_on = await is_on_repository.create_is_on(db, is_on)
    is_on_dict = model_to_dict(new_is_on)
    return IsOnBase(**is_on_dict)


@router.put(
    "/is_on/{is_on_id}", status_code=status.HTTP_200_OK, response_model=IsOnBase
)
async def update_is_on(
    is_on_id: int,
    is_on: IsOnBase,
    is_on_repository: IsOnRepository = Depends(IsOnRepository),
    db: AsyncSession = Depends(get_db),
) -> IsOnBase:
    updated_is_on = await is_on_repository.update_is_on(db, is_on_id, is_on)
    if updated_is_on is None:
        raise HTTPException(status_code=404, detail="is_on not found")
    is_on_dict = model_to_dict(updated_is_on)
    return IsOnBase(**is_on_dict)
