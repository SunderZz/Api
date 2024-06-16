import users.models as models
from typing import Annotated
from .schema import CustomersBase
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from database import engine2, AsyncSessionLocal
from common import model_to_dict
from .repository import CustomersRepository
from pay.router import create_pay
from payement.router import create_payment
from payement.schema import PaymentBase
from payement.repository import PaymentRepository
from pay.repository import PayRepository
from orders.schema import OrdersBase
from orders.repository import OrdersRepository
from orders.router import create_orders_from_user,update_orders

router = APIRouter(tags=["customers"])

@router.get("/customers/", status_code=status.HTTP_200_OK, response_model=list[CustomersBase])
async def get_customers(customers_repository: CustomersRepository = Depends(CustomersRepository),db:AsyncSession = Depends(get_db))-> list[CustomersBase]:
    customers = await customers_repository.get_customers(db)
    customers_list = [model_to_dict(customer) for customer in customers]
    return [CustomersBase(**customers_dict) for customers_dict in customers_list]


@router.get("/customers_by_id", response_model=CustomersBase)
async def get_customer_value(customers: int, customers_repository: CustomersRepository = Depends(CustomersRepository), db:AsyncSession = Depends(get_db)) -> CustomersBase:
    value = await customers_repository.get_customers_query(db, customers)
    if value is None:
        raise HTTPException(status_code=404, detail="customer not found or attribute not found")
    customers_dict = model_to_dict(value)
        
    return CustomersBase(**customers_dict)


@router.post("/customers/", status_code=status.HTTP_201_CREATED, response_model=CustomersBase)
async def create_customer(customer: CustomersBase,customers_repository: CustomersRepository = Depends(CustomersRepository), db:AsyncSession = Depends(get_db))-> CustomersBase:
    new_customer = await customers_repository.create_customers(db, customer)
    customers_dict = model_to_dict(new_customer) 
    return CustomersBase(**customers_dict)

@router.put("/customers/{customer_id}", status_code=status.HTTP_200_OK, response_model=CustomersBase)
async def update_customer(customer_id: int, customer: CustomersBase,customer_repository: CustomersRepository = Depends(CustomersRepository), db:AsyncSession = Depends(get_db))-> CustomersBase:
    updated_customer = await customer_repository.update_customers(db, customer_id, customer)
    if updated_customer is None:
        raise HTTPException(status_code=404, detail="customers not found")
    customer_dict = model_to_dict(updated_customer) 
    return CustomersBase(**customer_dict)

# @router.post("/customers/payment", status_code=status.HTTP_201_CREATED, response_model=CustomersBase)
# async def create_customer_payment(customer_id:int,pay:PaymentBase,customer: CustomersBase,customers_repository: CustomersRepository = Depends(CustomersRepository), db:AsyncSession = Depends(get_db))-> CustomersBase:
#     id_customer = await get_customer_value(customer_id,customers_repository,db)
#     buy = await create_pay(PaymentBase(Id_Orders=,Bills=,Status=,Amount=,Payment_Date=))
#     customers_dict = model_to_dict(new_customer) 
#     return CustomersBase(**customers_dict)

@router.post("/customers/orders", status_code=status.HTTP_201_CREATED, response_model=CustomersBase)
async def create_customer_orders(customer: CustomersBase,customers_repository: CustomersRepository = Depends(CustomersRepository), db:AsyncSession = Depends(get_db))-> CustomersBase:
    order = await create_orders_from_user()
    new_customer = await customers_repository.create_customers(db, customer)
    customers_dict = model_to_dict(new_customer) 
    return CustomersBase(**customers_dict)