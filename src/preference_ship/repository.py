from sqlalchemy.ext.asyncio import AsyncSession
from .models import Preferenceship
from sqlalchemy.future import select

class PreferenceshipRepository:

    async def create_preferenceship(self, db: AsyncSession, preferenceship: Preferenceship) -> Preferenceship:
        db_preferenceship = Preferenceship(**preferenceship.dict())
        db.add(db_preferenceship)
        await db.commit()
        await db.refresh(db_preferenceship)
        return db_preferenceship

    async def update_preferenceship(self, db: AsyncSession, preferenceship: int, db_preferenceship_data: Preferenceship) -> Preferenceship:
        result = await db.execute(select(Preferenceship).filter(Preferenceship.Id_Preferenceship == preferenceship))
        db_preferenceship = result.scalar_one_or_none()
        if db_preferenceship is None:
            return None
        for key, value in db_preferenceship_data.__dict__.items():
            if hasattr(db_preferenceship, key) and value is not None:
                setattr(db_preferenceship, key, value)
        await db.commit()
        return db_preferenceship
    
    async def create_preference_ship(self, db: AsyncSession, preferenceship: Preferenceship) -> Preferenceship:
        preferenceship_data = preferenceship.dict(by_alias=True)
        db_address = Preferenceship(**preferenceship_data)
        db.add(db_address)
        await db.commit()
        await db.refresh(db_address)
        return db_address
