from sqlalchemy.orm import Session
from .models import Season

class SeasonRepository:
    async def get_seasons(self, db: Session)->Season:
            return db.query(Season).first()
    
    async def create_season(self, db: Session, season: Season)->Season:
        db_season = Season(**season.dict())
        db.add(db_season)
        db.commit()
        db.refresh(db_season)
        return db_season

    async def update_season(self, db: Session, season_id: int, season_data: Season)->Season:
        db_season = db.query(Season).filter(Season.Id_Season == season_id).first()
        if db_season is None:
            return None
        for key, value in season_data.__dict__.items():
            if hasattr(db_season, key) and value is not None:
                setattr(db_season, key, value)
        db.commit()
        return db_season