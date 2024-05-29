from sqlalchemy.ext.asyncio import AsyncSession
from .models import Give
from sqlalchemy.future import select

class GiveRepository:

    async def create_give(self, db: AsyncSession, give: Give) -> Give:
        db_given = Give(**give.dict())
        db.add(db_given)
        await db.commit()
        await db.refresh(db_given)
        return db_given

    async def get_give(self, db: AsyncSession) -> list[Give]:
        result = await db.execute(select(Give))
        return result.scalars().all()

    async def get_give_by_id(self, db: AsyncSession, id: int) -> Give:
        result = await db.execute(select(Give).filter(Give.Id_Product == id))
        return result.scalar_one_or_none()

    async def update_give(self, db: AsyncSession, id: int, give: Give) -> Give:
        result = await db.execute(select(Give).filter(Give.Id_Product == id))
        db_given = result.scalar_one_or_none()
        if db_given:
            for key, value in give.dict().items():
                setattr(db_given, key, value)
            await db.commit()
            await db.refresh(db_given)
        return db_given
