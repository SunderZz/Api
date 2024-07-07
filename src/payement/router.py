from .schema import PaymentBase
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from .repository import PaymentRepository
from .services import (
    get_payments_service,
    get_payment_value_service,
    create_payment_service,
)

router = APIRouter(tags=["payment"])


@router.get(
    "/payment/", status_code=status.HTTP_200_OK, response_model=list[PaymentBase]
)
async def get_payments(
    payment_repository: PaymentRepository = Depends(PaymentRepository),
    db: AsyncSession = Depends(get_db),
) -> list[PaymentBase]:
    return await get_payments_service(payment_repository, db)


@router.get("/payment/{payment}", response_model=PaymentBase)
async def get_payment_value(
    payment: int,
    payment_repository: PaymentRepository = Depends(PaymentRepository),
    db: AsyncSession = Depends(get_db),
) -> PaymentBase:
    return await get_payment_value_service(payment, payment_repository, db)


@router.post(
    "/payment/", status_code=status.HTTP_201_CREATED, response_model=PaymentBase
)
async def create_payment(
    payment: PaymentBase,
    payment_repository: PaymentRepository = Depends(PaymentRepository),
    db: AsyncSession = Depends(get_db),
) -> PaymentBase:
    return await create_payment_service(payment, payment_repository, db)
