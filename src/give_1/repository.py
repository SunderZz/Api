from sqlalchemy.ext.asyncio import AsyncSession
from .models import Give_1
from sqlalchemy.future import select

class Give_1Repository:

    async def create_give_1(self, db: AsyncSession, given: Give_1) -> Give_1:
        db_given = Give_1(**given.dict())
        db.add(db_given)
        await db.commit()
        await db.refresh(db_given)
        return db_given

    async def get_give_1(self, db: AsyncSession) -> list[Give_1]:
        result = await db.execute(select(Give_1))
        return result.scalars().all()

    async def get_give_1_by_id(self, db: AsyncSession, id: int) -> Give_1:
        result = await db.execute(select(Give_1).filter(Give_1.Id_Notice == id))
        return result.scalar_one_or_none()

    async def update_give_1(self, db: AsyncSession, id: int, given: Give_1) -> Give_1:
        result = await db.execute(select(Give_1).filter(Give_1.Id_Notice == id))
        db_given = result.scalar_one_or_none()
        if db_given:
            for key, value in given.dict().items():
                setattr(db_given, key, value)
            await db.commit()
            await db.refresh(db_given)
        return db_given
