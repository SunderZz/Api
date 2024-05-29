from sqlalchemy.ext.asyncio import AsyncSession
from .models import Found
from sqlalchemy.future import select

class FoundRepository:

    async def create_found(self, db: AsyncSession, found: Found) -> Found:
        db_given = Found(**found.dict())
        db.add(db_given)
        await db.commit()
        await db.refresh(db_given)
        return db_given

    async def get_found(self, db: AsyncSession) -> list[Found]:
        result = await db.execute(select(Found))
        return result.scalars().all()

    async def get_found_by_id(self, db: AsyncSession, id: int) -> Found:
        result = await db.execute(select(Found).filter(Found.Id_Product == id))
        return result.scalar_one_or_none()

    async def update_found(self, db: AsyncSession, id: int, found: Found) -> Found:
        result = await db.execute(select(Found).filter(Found.Id_Product == id))
        db_given = result.scalar_one_or_none()
        if db_given:
            for key, value in found.dict().items():
                setattr(db_given, key, value)
            await db.commit()
            await db.refresh(db_given)
        return db_given
