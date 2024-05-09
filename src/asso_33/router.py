import season.models as models
import main as get_db
from typing import Annotated
from .schema import SeasonBase
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from database import engine, SessionLocal
from .repository import SeasonRepository
from common import model_to_dict

def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close_all()

router = APIRouter(tags=["season"])

models.Base.metadata.create_all(bind=engine)

db_dependency= Annotated[Session, Depends(get_db)]

@router.get("/season/", status_code=status.HTTP_200_OK, response_model=SeasonBase)
async def get_seasons(season_repository: SeasonRepository = Depends(SeasonRepository),db: Session = Depends(get_db))-> SeasonBase:
    seasons = await season_repository.get_seasons(db)
    season_dict = model_to_dict(seasons) 
    return SeasonBase(**season_dict)


@router.post("/season/", status_code=status.HTTP_201_CREATED, response_model=SeasonBase)
async def create_season(season: SeasonBase,season_repository: SeasonRepository = Depends(SeasonRepository), db: Session = Depends(get_db))-> SeasonBase:
    new_season = await season_repository.create_season(db, season)
    season_dict = model_to_dict(new_season) 
    return SeasonBase(**season_dict)

@router.put("/season/{season_id}", status_code=status.HTTP_200_OK, response_model=SeasonBase)
async def update_season(season_id: int, season: SeasonBase,season_repository: SeasonRepository = Depends(SeasonRepository), db: Session = Depends(get_db))-> SeasonBase:
    updated_season = await season_repository.update_season(db, season_id, season)
    if updated_season is None:
        raise HTTPException(status_code=404, detail="season not found")
    season_dict = model_to_dict(updated_season) 
    return SeasonBase(**season_dict)