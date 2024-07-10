from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from .repository import CustomersRepository
from .schema import CustomersBase
from common import model_to_dict


async def get_customers_service(
    customers_repository: CustomersRepository, db: AsyncSession
) -> list[CustomersBase]:
    customers = await customers_repository.get_customers(db)
    customers_list = [model_to_dict(customer) for customer in customers]
    return [CustomersBase(**customers_dict) for customers_dict in customers_list]


async def get_customer_value_service(
    customers: int, customers_repository: CustomersRepository, db: AsyncSession
) -> CustomersBase:
    value = await customers_repository.get_customers_query(db, customers)
    if value is None:
        raise HTTPException(
            status_code=404, detail="customer not found or attribute not found"
        )
    return CustomersBase(**model_to_dict(value))


async def create_customer_service(
    customer: CustomersBase, customers_repository: CustomersRepository, db: AsyncSession
) -> CustomersBase:
    new_customer = await customers_repository.create_customers(db, customer)
    return CustomersBase(**model_to_dict(new_customer))


async def update_customer_service(
    customer_id: int,
    customer: CustomersBase,
    customers_repository: CustomersRepository,
    db: AsyncSession,
) -> CustomersBase:
    updated_customer = await customers_repository.update_customers(
        db, customer_id, customer
    )
    if updated_customer is None:
        raise HTTPException(status_code=404, detail="customers not found")
    return CustomersBase(**model_to_dict(updated_customer))
