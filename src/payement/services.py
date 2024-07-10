from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from .repository import PaymentRepository
from .schema import PaymentBase
from common import model_to_dict


async def get_payments_service(
    payment_repository: PaymentRepository, db: AsyncSession
) -> list[PaymentBase]:
    payments = await payment_repository.get_payment(db)
    payment_list = [model_to_dict(payment) for payment in payments]
    return [PaymentBase(**payment_dict) for payment_dict in payment_list]


async def get_payment_value_service(
    payment: int, payment_repository: PaymentRepository, db: AsyncSession
) -> PaymentBase:
    value = await payment_repository.get_payment_query(db, payment)
    if value is None:
        raise HTTPException(
            status_code=404, detail="payment not found or attribute not found"
        )
    values = model_to_dict(value)
    return PaymentBase(**values)


async def create_payment_service(
    payment: PaymentBase, payment_repository: PaymentRepository, db: AsyncSession
) -> PaymentBase:
    new_payment = await payment_repository.create_payment(db, payment)
    payment_dict = model_to_dict(new_payment)
    return PaymentBase(**payment_dict)
