from fastapi import HTTPException, APIRouter, Depends, Form, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from users.schema import LogoutRequest, UserBase, UserCreate
from users.repository import UsersRepository
from database import get_db
from common import model_to_dict, validate_password
from users.services import (
    retrieve_user_address_service,
    create_user_type_service,
)
from users_adresses.router import (
    get_user_addresse,
)
from adresse_types.router import (
    create_adresse_type,
)
from producers.router import (
    get_user_by_producer,
)
from customers.repository import CustomersRepository
from producers.repository import ProducersRepository
from adresse_types.schema import AdresseTypeBase
from adresse_types.repository import AdresseTypesRepository

from users_adresses.schema import UsersAdressesBase
from users_adresses.repository import UsersAdressesRepository


router = APIRouter(tags=["users"])


@router.get(
    "/users/{user_id}",
    response_model=UserBase,
    description="retrieve informations of an user",
)
async def get_user(
    user_id: int,
    user_repository: UsersRepository = Depends(UsersRepository),
    db: AsyncSession = Depends(get_db),
) -> UserBase:
    user = await user_repository.get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    user_dict = model_to_dict(user)
    return UserBase(**user_dict)


@router.get(
    "/users_by_token",
    response_model=UserBase,
    description="retrieve informations of an user with token",
)
async def get_user_by_token(
    token: str,
    user_repository: UsersRepository = Depends(UsersRepository),
    db: AsyncSession = Depends(get_db),
) -> UserBase:
    user = await user_repository.get_user_with_token(db, token)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    user_dict = model_to_dict(user)
    return UserBase(**user_dict)


@router.get(
    "/users", response_model=list[UserBase], description="get all user information"
)
async def get_users(
    user_repository: UsersRepository = Depends(UsersRepository),
    db: AsyncSession = Depends(get_db),
) -> list[UserBase]:
    users = await user_repository.get_all_users(db)
    users_dict = [model_to_dict(user) for user in users]
    return [UserBase(**user_dict) for user_dict in users_dict]


@router.post("/users/login", response_model=UserBase)
async def login_user(
    mail: str,
    password: str,
    user_repository: UsersRepository = Depends(UsersRepository),
    db: AsyncSession = Depends(get_db),
) -> UserBase:
    user = await user_repository.authenticate_user(db, mail, password)
    if user is None:
        raise HTTPException(status_code=404, detail="Invalid credentials")
    user_dict = model_to_dict(user)
    return UserBase(**user_dict)


@router.delete("/users/logout", status_code=200)
async def logout_user(
    logout_request: LogoutRequest,
    user_repository: UsersRepository = Depends(UsersRepository),
    db: AsyncSession = Depends(get_db),
) -> None:
    user = await user_repository.get_user(db, logout_request.user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    await user_repository.delete_token(db, logout_request.user_id)
    return


@router.post("/users/", response_model=UserBase)
async def create_user_type(
    firstName: str = Form(...),
    lastName: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    summary: Optional[str] = Form(None),
    isFarmer: bool = Form(...),
    document: Optional[UploadFile] = File(None),
    user_repository: UsersRepository = Depends(UsersRepository),
    customers_repository: CustomersRepository = Depends(CustomersRepository),
    producers_repository: ProducersRepository = Depends(ProducersRepository),
    db: AsyncSession = Depends(get_db),
) -> UserBase:
    user = UserCreate(F_Name=firstName, Name=lastName, Mail=email, Password=password)

    if not validate_password(user.Password):
        raise HTTPException(
            status_code=400,
            detail="Password must contain at least one uppercase letter, two digits, and one special character.",
        )
    user_post = await user_repository.create_user(db, user)
    user_dict = model_to_dict(user_post)
    user_id = UserBase(**user_dict)

    await create_user_type_service(
        firstName,
        lastName,
        email,
        password,
        summary,
        isFarmer,
        document,
        user_id,
        producers_repository,
        customers_repository,
        db,
    )
    return user_id


@router.get("/adresse_of_user", response_model=list[UsersAdressesBase])
async def retrieve_adresse_information(
    adresse_id: int,
    user_adresse_repository: UsersAdressesRepository = Depends(UsersAdressesRepository),
    db: AsyncSession = Depends(get_db),
) -> list[UsersAdressesBase]:
    db_address = await get_user_addresse(adresse_id, user_adresse_repository, db)
    return db_address


@router.get(
    "/users/{user_id}/addresses",
    response_model=list[UsersAdressesBase] | UsersAdressesBase,
)
async def retrieve_user_address(
    user_id: int,
    user_adresse_repository: UsersAdressesRepository = Depends(UsersAdressesRepository),
    adresse_type_repository: AdresseTypesRepository = Depends(AdresseTypesRepository),
    db: AsyncSession = Depends(get_db),
) -> list[UsersAdressesBase] | UsersAdressesBase:
    return await retrieve_user_address_service(
        db, user_id, user_adresse_repository, adresse_type_repository
    )


@router.post("/users/{user_id}/addresses", response_model=AdresseTypeBase)
async def create_address_type_for_user(
    adresse_type: AdresseTypeBase,
    adresse_type_repository: AdresseTypesRepository = Depends(AdresseTypesRepository),
    db: AsyncSession = Depends(get_db),
) -> AdresseTypeBase:
    db_address = await create_adresse_type(adresse_type, adresse_type_repository, db)
    return db_address


@router.get(
    "/user_by_producer",
    response_model=UserBase,
    description="retrieve informations of an user",
)
async def get_user(
    producer_id: int,
    user_repository: UsersRepository = Depends(UsersRepository),
    producer_repository: ProducersRepository = Depends(ProducersRepository),
    db: AsyncSession = Depends(get_db),
) -> UserBase:
    test = await get_user_by_producer(producer_id, producer_repository, db)
    user_query = test.Id_Users
    user = await user_repository.get_user(db, user_query)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    user_dict = model_to_dict(user)
    return UserBase(**user_dict)
