from sqlalchemy.ext.asyncio import AsyncSession
from .models import Located
from sqlalchemy.future import select

class LocatedRepository:

    async def create_located(self, db: AsyncSession, located: Located) -> Located:
        db_located = Located(**located.dict())
        db.add(db_located)
        await db.commit()
        await db.refresh(db_located)
        return db_located

    async def get_located(self, db: AsyncSession) -> list[Located]:
        result = await db.execute(select(Located))
        return result.scalars().all()

    async def get_located_by_id(self, db: AsyncSession, id: int) -> Located:
        result = await db.execute(select(Located).filter(Located.Id_Users_adresses == id))
        return result.scalar_one_or_none()

    async def update_located(self, db: AsyncSession, id: int, located: Located) -> Located:
        result = await db.execute(select(Located).filter(Located.Id_Users_adresses == id))
        db_located = result.scalar_one_or_none()
        if db_located:
            for key, value in located.dict().items():
                setattr(db_located, key, value)
            await db.commit()
            await db.refresh(db_located)
        return db_located
