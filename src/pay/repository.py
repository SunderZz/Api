from sqlalchemy.ext.asyncio import AsyncSession
from .models import Pay
from sqlalchemy.future import select


class PayRepository:

    async def create_pay(self, db: AsyncSession, pay: Pay) -> Pay:
        db_pay = Pay(**pay.dict())
        db.add(db_pay)
        await db.commit()
        await db.refresh(db_pay)
        return db_pay

    async def get_pays(self, db: AsyncSession) -> list[Pay]:
        result = await db.execute(select(Pay))
        return result.scalars().all()

    async def get_pay_by_id(self, db: AsyncSession, id: int) -> Pay:
        result = await db.execute(select(Pay).filter(Pay.Id_Payments == id))
        return result.scalar_one_or_none()

    async def update_pay(self, db: AsyncSession, id: int, pay: Pay) -> Pay:
        result = await db.execute(select(Pay).filter(Pay.Id_Payments == id))
        db_pay = result.scalar_one_or_none()
        if db_pay:
            for key, value in pay.dict().items():
                setattr(db_pay, key, value)
            await db.commit()
            await db.refresh(db_pay)
        return db_pay
