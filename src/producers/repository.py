from sqlalchemy.ext.asyncio import AsyncSession
from .models import Producers
from sqlalchemy.future import select

class ProducersRepository:
    async def get_producers(self, db: AsyncSession) -> list[Producers]:
        result = await db.execute(select(Producers))
        return result.scalars().all()
    
    async def get_producers_query(self, db: AsyncSession, producers: int) -> Producers:
        result = await db.execute(select(Producers).filter(Producers.Id_Producers == producers))
        return result.scalar_one_or_none()

    async def create_producers(self, db: AsyncSession, producers: Producers) -> Producers:
        db_producers = Producers(**producers.dict())
        db.add(db_producers)
        await db.commit()
        await db.refresh(db_producers)
        return db_producers

    async def update_producers(self, db: AsyncSession, producers: int, db_producers_data: Producers) -> Producers:
        result = await db.execute(select(Producers).filter(Producers.Id_Producers == producers))
        db_producers = result.scalar_one_or_none()
        if db_producers is None:
            return None
        for key, value in db_producers_data.__dict__.items():
            if hasattr(db_producers, key) and value is not None:
                setattr(db_producers, key, value)
        await db.commit()
        return db_producers
