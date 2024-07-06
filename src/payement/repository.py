from sqlalchemy.ext.asyncio import AsyncSession
from .models import Payment
from sqlalchemy.future import select


class PaymentRepository:
    async def get_payment(self, db: AsyncSession) -> list[Payment]:
        result = await db.execute(select(Payment))
        return result.scalars().all()

    async def get_payment_query(self, db: AsyncSession, payment: int) -> Payment:
        result = await db.execute(
            select(Payment).filter(Payment.Id_Payments == payment)
        )
        return result.scalar_one_or_none()

    async def create_payment(self, db: AsyncSession, payment: Payment) -> Payment:
        db_payment = Payment(**payment.dict())
        db.add(db_payment)
        await db.commit()
        await db.refresh(db_payment)
        return db_payment

    async def update_payment(
        self, db: AsyncSession, payment_id: int, db_payment_data: Payment
    ) -> Payment:
        result = await db.execute(
            select(Payment).filter(Payment.Id_Payments == payment_id)
        )
        db_payment = result.scalar_one_or_none()
        if db_payment is None:
            return None
        for key, value in db_payment_data.__dict__.items():
            if hasattr(db_payment, key) and value is not None:
                setattr(db_payment, key, value)
        await db.commit()
        return db_payment
