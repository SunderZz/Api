from sqlalchemy.ext.asyncio import AsyncSession
from .models import Got
from sqlalchemy.future import select


class GotRepository:

    async def create_got(self, db: AsyncSession, got: Got) -> Got:
        db_Got = Got(**got.dict())
        db.add(db_Got)
        await db.commit()
        await db.refresh(db_Got)
        return db_Got

    async def get_got(self, db: AsyncSession) -> list[Got]:
        result = await db.execute(select(Got))
        return result.scalars().all()

    async def get_got_by_id(self, db: AsyncSession, id: int) -> list[Got]:
        result = await db.execute(select(Got).filter(Got.Id_Code_Postal == id))
        return result.scalars().all()

    async def update_got(
        self, db: AsyncSession, got: Got, id: int | None = None
    ) -> Got:
        result = await db.execute(select(Got).filter(Got.Id_City == id))
        db_Got = result.scalar_one_or_none()
        if db_Got:
            for key, value in got.dict().items():
                setattr(db_Got, key, value)
            await db.commit()
            await db.refresh(db_Got)
        return db_Got
