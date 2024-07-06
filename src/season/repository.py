from sqlalchemy.ext.asyncio import AsyncSession
from .models import Season
from sqlalchemy.future import select


class SeasonRepository:
    async def get_seasons(self, db: AsyncSession) -> Season:
        result = await db.execute(select(Season))
        return result.scalars().all()

    async def get_season_by_id(self, db: AsyncSession, id: int) -> Season:
        result = await db.execute(select(Season).filter(Season.Id_Season == id))
        return result.scalar_one_or_none()

    async def get_season_by_name(self, db: AsyncSession, name: str) -> Season:
        result = await db.execute(select(Season).filter(Season.Name == name))
        return result.scalar_one_or_none()

    async def create_season(self, db: AsyncSession, season: Season) -> Season:
        db_season = Season(**season.dict())
        db.add(db_season)
        await db.commit()
        await db.refresh(db_season)
        return db_season

    async def update_season(
        self, db: AsyncSession, season_id: int, season_data: Season
    ) -> Season:
        result = await db.execute(select(Season).filter(Season.Id_Season == season_id))
        db_season = result.scalar_one_or_none()
        if db_season is None:
            return None
        for key, value in season_data.__dict__.items():
            if hasattr(db_season, key) and value is not None:
                setattr(db_season, key, value)
        await db.commit()
        return db_season
