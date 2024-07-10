from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import UploadFile
from adresse_types.router import (
    get_adresse_types_by_user,
)
from adresse_types.repository import AdresseTypesRepository
from users_adresses.router import (
    get_user_addresse,
)
from users_adresses.schema import UsersAdressesBase
from users_adresses.repository import UsersAdressesRepository
from customers.router import create_customer
from customers.schema import CustomersUserBase
from customers.repository import CustomersRepository
from producers.router import create_producer
from producers.schema import ProducersCreateBase
from producers.repository import ProducersRepository


from users.schema import UserBase


async def retrieve_user_address_service(
    user_id: int,
    user_adresse_repository: UsersAdressesRepository,
    adresse_type_repository: AdresseTypesRepository,
    db: AsyncSession,
) -> list[UsersAdressesBase]:
    adresse_type = await get_adresse_types_by_user(user_id, adresse_type_repository, db)
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
