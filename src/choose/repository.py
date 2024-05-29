from sqlalchemy.ext.asyncio import AsyncSession
from .models import Choose
from sqlalchemy.future import select

class ChooseRepository:

    async def create_choose(self, db: AsyncSession, choose: Choose) -> Choose:
        db_given = Choose(**choose.dict())
        db.add(db_given)
        await db.commit()
        await db.refresh(db_given)
        return db_given

    async def get_choose(self, db: AsyncSession) -> list[Choose]:
        result = await db.execute(select(Choose))
        return result.scalars().all()

    async def get_choose_by_id(self, db: AsyncSession, id: int) -> Choose:
        result = await db.execute(select(Choose).filter(Choose.Id_Product == id))
        return result.scalar_one_or_none()

    async def update_choose(self, db: AsyncSession, id: int, choose: Choose) -> Choose:
        result = await db.execute(select(Choose).filter(Choose.Id_Product == id))
        db_given = result.scalar_one_or_none()
        if db_given:
            for key, value in choose.dict().items():
                setattr(db_given, key, value)
            await db.commit()
            await db.refresh(db_given)
        return db_given
