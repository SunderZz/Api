from sqlalchemy.ext.asyncio import AsyncSession
from .models import Is_On
from sqlalchemy.future import select


class IsOnRepository:

    async def create_is_on(self, db: AsyncSession, is_On: Is_On) -> Is_On:
        db_is_On = Is_On(**is_On.dict())
        db.add(db_is_On)
        await db.commit()
        await db.refresh(db_is_On)
        return db_is_On

    async def get_is_on(self, db: AsyncSession) -> list[Is_On]:
        result = await db.execute(select(Is_On))
        return result.scalars().all()

    async def get_is_on_by_id(self, db: AsyncSession, id: int) -> list[Is_On]:
        result = await db.execute(select(Is_On).filter(Is_On.Id_Season == id))
        return result.scalars().all()

    async def get_season_with_produt(self, db: AsyncSession, id: int) -> Is_On:
        result = await db.execute(select(Is_On).filter(Is_On.Id_Product == id))
        return result.scalar_one_or_none()

    async def update_is_on(self, db: AsyncSession, id: int, is_On: Is_On) -> Is_On:
        result = await db.execute(select(Is_On).filter(Is_On.Id_Product == id))
        db_is_On = result.scalar_one_or_none()
        if db_is_On:
            for key, value in is_On.dict().items():
                setattr(db_is_On, key, value)
            await db.commit()
            await db.refresh(db_is_On)
        return db_is_On
