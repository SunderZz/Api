from .schema import CustomersBase,CustomersUserBase
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from .repository import CustomersRepository
from .services import (
    get_customers_service,
    get_customer_value_service,
    get_user_value_service,
    create_customer_service,
    update_customer_service,
)
from orders.router import create_orders_from_user

router = APIRouter(tags=["customers"])


@router.get(
    "/customers/", status_code=status.HTTP_200_OK, response_model=list[CustomersBase]
)
async def get_customers(
    customers_repository: CustomersRepository = Depends(CustomersRepository),
    db: AsyncSession = Depends(get_db),
) -> list[CustomersBase]:
    return await get_customers_service(customers_repository, db)


@router.get("/user_by_id", response_model=CustomersBase)
async def get_user_value(
    customers: int,
    customers_repository: CustomersRepository = Depends(CustomersRepository),
    db: AsyncSession = Depends(get_db),
) -> CustomersBase:
    return await get_user_value_service(customers, customers_repository, db)

@router.get("/customers_by_id", response_model=CustomersUserBase)
async def get_customer_value(
    customers: int,
    customers_repository: CustomersRepository = Depends(CustomersRepository),
    db: AsyncSession = Depends(get_db),
) -> CustomersUserBase:
    return await get_customer_value_service(customers, customers_repository, db)


@router.post(
    "/customers/", status_code=status.HTTP_201_CREATED, response_model=CustomersBase
)
async def create_customer(
    customer: CustomersBase,
    customers_repository: CustomersRepository = Depends(CustomersRepository),
    db: AsyncSession = Depends(get_db),
) -> CustomersBase:
    return await create_customer_service(customer, customers_repository, db)


@router.put(
    "/customers/{customer_id}",
    status_code=status.HTTP_200_OK,
    response_model=CustomersBase,
)
async def update_customer(
    customer_id: int,
    customer: CustomersBase,
    customers_repository: CustomersRepository = Depends(CustomersRepository),
    db: AsyncSession = Depends(get_db),
) -> CustomersBase:
    return await update_customer_service(
        customer_id, customer, customers_repository, db
    )


@router.post(
    "/customers/orders",
    status_code=status.HTTP_201_CREATED,
    response_model=CustomersBase,
)
async def create_customer_orders(
    customer: CustomersBase,
    customers_repository: CustomersRepository = Depends(CustomersRepository),
    db: AsyncSession = Depends(get_db),
) -> CustomersBase:
    order = await create_orders_from_user()
    new_customer = await create_customer_service(customer, customers_repository, db)
    return new_customer


# @router.post("/customers/payment", status_code=status.HTTP_201_CREATED, response_model=CustomersBase)
# async def create_customer_payment(customer_id:int,pay:PaymentBase,customer: CustomersBase,customers_repository: CustomersRepository = Depends(CustomersRepository), db:AsyncSession = Depends(get_db))-> CustomersBase:
#     id_customer = await get_customer_value(customer_id,customers_repository,db)
#     buy = await create_pay(PaymentBase(Id_Orders=,Bills=,Status=,Amount=,Payment_Date=))
#     customers_dict = model_to_dict(new_customer)
#     return CustomersBase(**customers_dict)
