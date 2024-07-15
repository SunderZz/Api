from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, UploadFile
from adresse_types.router import (
    get_adresse_types_by_user,
)
from adresse_types.repository import AdresseTypesRepository
from users_adresses.router import (
    get_user_addresse,
)
from users_adresses.schema import UsersAdressesBase
from users_adresses.repository import UsersAdressesRepository
from customers.router import create_customer, get_customer_value, update_customer
from customers.schema import CustomersUserBase
from customers.repository import CustomersRepository
from producers.router import create_producer, get_producer_by_user, update_producer
from producers.schema import ProducersCreateBase, ProducersModifyBase
from producers.repository import ProducersRepository


from users.schema import UserBase


async def retrieve_user_address_service(
    db: AsyncSession,
    user_id: int,
    user_adresse_repository: UsersAdressesRepository = Depends(UsersAdressesRepository),
    adresse_type_repository: AdresseTypesRepository = Depends(AdresseTypesRepository),
) -> list[UsersAdressesBase] | UsersAdressesBase:
    adresse_type = await get_adresse_types_by_user(user_id, db, adresse_type_repository)
    db_address = await get_user_addresse(
        adresse_type.Id_Users_adresses, user_adresse_repository, db
    )
    return db_address


async def create_user_type_service(
    firstName: str,
    lastName: str,
    email: str,
    password: str,
    summary: Optional[str],
    isFarmer: bool,
    document: Optional[UploadFile],
    user_id: UserBase,
    producers_repository: ProducersRepository,
    customers_repository: CustomersRepository,
    db: AsyncSession,
):
    if isFarmer and document:
        document_content = await document.read()
        await create_producer(
            ProducersCreateBase(
                Id_Users=user_id.Id_Users,
                description=summary,
                Document=document_content,
            ),
            producers_repository,
            db,
        )
    else:
        await create_customer(
            CustomersUserBase(Id_Users=user_id.Id_Users), customers_repository, db
        )


async def modify_user_type_service(
    firstName: str,
    lastName: str,
    email: str,
    password: str,
    summary: Optional[str],
    isFarmer: bool,
    document: Optional[UploadFile],
    user_id: UserBase,
    producers_repository: ProducersRepository,
    customers_repository: CustomersRepository,
    db: AsyncSession,
):
    if isFarmer:
        document_content = None
        if document:
            document_content = await document.read()

        producers_id = await get_producer_by_user(
            user_id.Id_Users, producers_repository, db
        )
        await update_producer(
            producers_id.Id_Producers,
            ProducersModifyBase(
                Id_Users=user_id.Id_Users,
                description=summary,
                Document=document_content,
            ),
            producers_repository,
            db,
        )
    else:
        customer_id = await get_customer_value(
            user_id.Id_Users, customers_repository, db
        )
        await update_customer(
            customer_id.Id_Casual,
            CustomersUserBase(Id_Users=user_id.Id_Users),
            customers_repository,
            db,
        )
