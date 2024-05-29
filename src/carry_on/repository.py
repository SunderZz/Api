from sqlalchemy.ext.asyncio import AsyncSession
from .models import CarryOn
from sqlalchemy.future import select

class CarryOnRepository:

    async def create_carry_on(self, db: AsyncSession, carry_on: CarryOn) -> CarryOn:
        db_given = CarryOn(**carry_on.dict())
        db.add(db_given)
        await db.commit()
        await db.refresh(db_given)
        return db_given

    async def get_carry_on(self, db: AsyncSession) -> list[CarryOn]:
        result = await db.execute(select(CarryOn))
        return result.scalars().all()

    async def get_carry_on_by_id(self, db: AsyncSession, id: int) -> CarryOn:
        result = await db.execute(select(CarryOn).filter(CarryOn.Id_Producers == id))
        return result.scalar_one_or_none()

    async def update_carry_on(self, db: AsyncSession, id: int, carry_on: CarryOn) -> CarryOn:
        result = await db.execute(select(CarryOn).filter(CarryOn.Id_Producers == id))
        db_given = result.scalar_one_or_none()
        if db_given:
            for key, value in carry_on.dict().items():
                setattr(db_given, key, value)
            await db.commit()
            await db.refresh(db_given)
        return db_given
