import users.models as models
from typing import Annotated
from .schema import PaymentBase
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from database import engine2, AsyncSessionLocal
from .repository import PaymentRepository
from common import model_to_dict

router = APIRouter(tags=["payement"])



@router.get("/payment/", status_code=status.HTTP_200_OK, response_model=list[PaymentBase])
async def get_payments(payment_repository: PaymentRepository = Depends(PaymentRepository),db:AsyncSession = Depends(get_db))-> list[PaymentBase]:
    payments = await payment_repository.get_payment(db)
    payment_list = [model_to_dict(payment) for payment in payments]
    return [PaymentBase(**payment_dict) for payment_dict in payment_list]


@router.get("/payment/{payment}", response_model=PaymentBase)
async def get_payment_value(payment: str, payment_repository: PaymentRepository = Depends(PaymentRepository), db:AsyncSession = Depends(get_db)) -> PaymentBase:
    value = await payment_repository.get_payment_query(db, payment)
    if value is None:
        raise HTTPException(status_code=404, detail="payment not found or attribute not found")
    return PaymentBase(value=value)


@router.post("/payment/", status_code=status.HTTP_201_CREATED, response_model=PaymentBase)
async def create_payment(payment: PaymentBase,payment_repository: PaymentRepository = Depends(PaymentRepository), db:AsyncSession = Depends(get_db))-> PaymentBase:
    new_payment = await payment_repository.create_payment(db, payment)
    payment_dict = model_to_dict(new_payment) 
    return PaymentBase(**payment_dict)

@router.put("/payment/{payment_id}", status_code=status.HTTP_200_OK, response_model=PaymentBase)
async def update_payment(payment_id: int, payment: PaymentBase,payment_repository: PaymentRepository = Depends(PaymentRepository), db:AsyncSession = Depends(get_db))-> PaymentBase:
    updated_payment = await payment_repository.update_payment(db, payment_id, payment)
    if updated_payment is None:
        raise HTTPException(status_code=404, detail="payment not found")
    payment_dict = model_to_dict(updated_payment) 
    return PaymentBase(**payment_dict)