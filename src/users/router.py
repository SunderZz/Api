import users.models as models
from database import get_db
from typing import Annotated, Optional
from .schema import LogoutRequest, UserBase,UserCreate, UserModify
from fastapi import APIRouter,  Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from database import engine2, AsyncSessionLocal
from .repository import UsersRepository
from common import model_to_dict, validate_password

from adresse_types.router import create_adresses_types, update_adresse_type, get_adresses_type_user,update_adresse_type
from adresse_types.schema import AdresseTypeBase
from adresse_types.repository import AdresseTypesRepository
from users_adresses.router import create_user_an_address,update_user_address, get_user_addresses
from users_adresses.schema import UsersAdressesBase, UsersCreateAdressesBase
from users_adresses.repository import UsersAdressesRepository
from located.repository import LocatedRepository
from code_postal.schema import CodePostalBase
from code_postal.repository import CodePostalRepository
from located.router import get_located_by_ids
from city.schema import CityBase
from got_3.repository import GotRepository
from city.repository import CityRepository
from preference_ship.repository import PreferenceshipRepository
from asso_33.repository import Asso_33Repository
from customers.router import create_customer, update_customer, get_customer_value
from customers.schema import CustomersUserBase
from customers.repository import CustomersRepository
from producers.router import create_producer, update_producer, get_producer_value
from producers.schema import ProducersCreateBase, ProducersModifyBase
from producers.repository import ProducersRepository

router = APIRouter(tags=["users"])

@router.get("/users/{user_id}", response_model=UserBase)
async def get_user( user_id: int, user_repository: UsersRepository = Depends(UsersRepository), db:AsyncSession = Depends(get_db))-> UserBase:
    user = await user_repository.get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    user_dict = model_to_dict(user) 
    return UserBase(**user_dict)

@router.get("/users_by_token", response_model=UserBase)
async def get_user_by_token( token: str, user_repository: UsersRepository = Depends(UsersRepository), db:AsyncSession = Depends(get_db))-> UserBase:
    user = await user_repository.get_user_token(db, token)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    user_dict = model_to_dict(user) 
    return UserBase(**user_dict)

@router.get("/users", response_model=list[UserBase])
async def get_users(user_repository: UsersRepository = Depends(UsersRepository), db:AsyncSession = Depends(get_db)) -> list[UserBase]:
    users = await user_repository.get_all_users(db)
    users_dict = [model_to_dict(user) for user in users]
    return [UserBase(**user_dict) for user_dict in users_dict]

@router.post("/users/login", response_model=UserBase)
async def login_user(
    mail: str,
    password: str,
    user_repository: UsersRepository = Depends(UsersRepository),
    db:AsyncSession = Depends(get_db)
) -> UserBase:
    user = await user_repository.authenticate_user(db, mail, password)
    if user is None:
        raise HTTPException(status_code=404, detail="Invalid credentials")
    user_dict = model_to_dict(user)
    return UserBase(**user_dict)

@router.post("/users/logout", status_code=200)
async def logout_user(
    logout_request: LogoutRequest,
    user_repository: UsersRepository = Depends(UsersRepository),
    db: AsyncSession = Depends(get_db)
)-> None:
    user = await user_repository.get_user(db, logout_request.user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.token = None
    await db.commit()
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
    db: AsyncSession = Depends(get_db)
) -> UserBase:
    user = UserCreate(
        F_Name=firstName,
        Name=lastName,
        Mail=email,
        Password=password
    )
    
    if not validate_password(user.Password):
        raise HTTPException(status_code=400, detail="Password must contain at least one uppercase letter, two digits, and one special character.")

    user_post = await user_repository.create_user(db, user)
    user_dict = model_to_dict(user_post) 
    user_id = UserBase(**user_dict)
    if isFarmer and document:
        document_content = await document.read()
        await create_producer(ProducersCreateBase(Id_Users=user_id.Id_Users, description=summary, Document=document_content), producers_repository, db)
    else:
        print(user_id)
        await create_customer(CustomersUserBase(Id_Users=user_id.Id_Users), customers_repository, db)
    
    user_dict = model_to_dict(user_post)
    return UserBase(**user_dict)

@router.put("/users/{user_id}", response_model=UserBase)
async def update_user_type(
    user_id: int,
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
    db: AsyncSession = Depends(get_db)
) -> UserBase:
    user = UserModify(
        F_Name=firstName,
        Name=lastName,
        Mail=email,
        Password=password
    )
    
    if not validate_password(user.Password):
        raise HTTPException(status_code=400, detail="Password must contain at least one uppercase letter, two digits, and one special character.")

    user_post = await user_repository.update_user(db, user_id, user)
    if user_post is None:
        raise HTTPException(status_code=404, detail="User not found")

    user_dict = model_to_dict(user_post)
    user_result = UserBase(**user_dict)
    
    if isFarmer and document:
        document_content = await document.read()
        producers_id = await get_producer_value(user_result.Id_Users, producers_repository, db)
        await update_producer(producers_id.Id_Producers,ProducersModifyBase(Id_Users=user_result.Id_Users, description=summary, Document=document_content), producers_repository, db)
    else:
        customer_id = await get_customer_value(user_result.Id_Users, customers_repository, db)
        await update_customer(customer_id.Id_Casual,CustomersUserBase(Id_Users=user_result.Id_Users), customers_repository, db)
    
    user_dict = model_to_dict(user_post)
    return UserBase(**user_dict)


@router.post("/users/addresses/{user_id}", response_model=UsersCreateAdressesBase)
async def create_new_user_address(authorize:bool,adresse:UsersAdressesBase,city:CityBase,code_postal:CodePostalBase,got_repository:GotRepository= Depends(GotRepository),city_repository:CityRepository= Depends(CityRepository),code_postal_repository:CodePostalRepository= Depends(CodePostalRepository),located_repository:LocatedRepository= Depends(LocatedRepository),user_adresse_repository: UsersAdressesRepository = Depends(UsersAdressesRepository),asso_33_repository: Asso_33Repository = Depends(Asso_33Repository),preference_ship_repository: PreferenceshipRepository = Depends(PreferenceshipRepository),
 db:AsyncSession = Depends(get_db)) -> UsersCreateAdressesBase:
    db_address = await create_user_an_address(authorize,adresse,code_postal,city,got_repository,asso_33_repository,preference_ship_repository,city_repository,code_postal_repository,located_repository, user_adresse_repository,db)
    return db_address

@router.put("/users/{adresses_id}/addresses", response_model=UsersAdressesBase)
async def modify_user_address(authorize:bool,user_id: int, addresses_id: int, adresse: UsersAdressesBase, adresse_type: AdresseTypeBase, code_postal: Optional[int] = None,city: Optional[str] = None,got_repository:GotRepository= Depends(GotRepository),city_repository:CityRepository= Depends(CityRepository), located_repository: LocatedRepository = Depends(LocatedRepository), code_postal_repository: CodePostalRepository = Depends(CodePostalRepository), user_adresse_repository: UsersAdressesRepository = Depends(UsersAdressesRepository), adresse_type_repository: AdresseTypesRepository = Depends(AdresseTypesRepository), db:AsyncSession = Depends(get_db)) -> UsersAdressesBase:
    code =await get_located_by_ids(addresses_id,located_repository,db)
    code_postal_unchange = code.Id_Code_Postal
    if not code_postal:
        code_postal=code_postal_unchange
    db_address = await update_user_address(authorize,addresses_id,adresse,code_postal,city,got_repository,city_repository,code_postal_repository, user_adresse_repository,located_repository,db)
    adresse_type = await adresse_type_repository.get_adressestypes_user(db, user_id)
    await update_adresse_type(adresse_type.Id_Adresse_Type,adresse_type,adresse_type_repository,db)
    return db_address

@router.get("/adresse_of_user", response_model=list[UsersAdressesBase])
async def retrieve_adresse_information(adresse_id:int,user_adresse_repository: UsersAdressesRepository = Depends(UsersAdressesRepository),adresse_type_repository: AdresseTypesRepository = Depends(AdresseTypesRepository), db:AsyncSession = Depends(get_db)) -> list[UsersAdressesBase]:
    db_address = await get_user_addresses(adresse_id, user_adresse_repository,db)
    return db_address

@router.get("/users/{user_id}/addresses", response_model=list[UsersAdressesBase])
async def retrieve_user_address(user_id:int,user_adresse_repository: UsersAdressesRepository = Depends(UsersAdressesRepository),adresse_type_repository: AdresseTypesRepository = Depends(AdresseTypesRepository), db:AsyncSession = Depends(get_db)) -> list[UsersAdressesBase]:
    adresse_type = await get_adresses_type_user(user_id,adresse_type_repository,db)
    db_address = await get_user_addresses(adresse_type.Id_Users_adresses, user_adresse_repository,db)
    return db_address

@router.post("/users/{user_id}/addresses", response_model=AdresseTypeBase)
async def create_address_type_for_user(user_id:int,adresse_type:AdresseTypeBase,user_adresse_repository: UsersAdressesRepository = Depends(UsersAdressesRepository),adresse_type_repository: AdresseTypesRepository = Depends(AdresseTypesRepository),db:AsyncSession = Depends(get_db)) -> AdresseTypeBase:
    db_address = await create_adresses_types(user_id,adresse_type, adresse_type_repository,db)
    return db_address

@router.put("/users/{adresse_id}/addresses", response_model=list[UsersAdressesBase])
async def update_user_adresse_type(adresse_id:int,adresse_type:AdresseTypeBase,user_adresse_repository: UsersAdressesRepository = Depends(UsersAdressesRepository),adresse_type_repository: AdresseTypesRepository = Depends(AdresseTypesRepository), db:AsyncSession = Depends(get_db)) -> list[UsersAdressesBase]:
    db_address = await update_adresse_type(adresse_id,adresse_type ,user_adresse_repository,db)
    return db_address