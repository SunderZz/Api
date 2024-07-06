from sqlalchemy.ext.asyncio import AsyncSession
from .models import Unit
from sqlalchemy.future import select


class UnitRepository:
    async def get_units(self, db: AsyncSession) -> Unit:
        result = await db.execute(select(Unit))
        return result.scalars().all()

    async def create_unit(self, db: AsyncSession, unit: Unit) -> Unit:
        db_unit = Unit(**unit.dict())
        db.add(db_unit)
        await db.commit()
        await db.refresh(db_unit)
        return db_unit

    async def update_unit(
        self, db: AsyncSession, unit_id: int, unit_data: Unit
    ) -> Unit:
        result = await db.execute(select(Unit).filter(Unit.Id_Unit == unit_id))
        db_unit = result.scalar_one_or_none()
        if db_unit is None:
            return None
        for key, value in unit_data.__dict__.items():
            if hasattr(db_unit, key) and value is not None:
                setattr(db_unit, key, value)
        await db.commit()
        return db_unit
