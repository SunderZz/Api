import users.models as models
import main as get_db
from typing import Annotated
from .schema import UserBase
from fastapi import APIRouter,  Depends, HTTPException
from sqlalchemy.orm import Session
from database import engine, SessionLocal
from .repository import UsersRepository
from common import model_to_dict

from adresse_types.router import create_adresses_types, update_adresse_type, get_adresses_type_user,update_adresse_type
from adresse_types.schema import AdresseTypeBase
from adresse_types.repository import AdresseTypesRepository
from users_adresses.router import create_user_address,update_user_address, get_user_addresses
from users_adresses.schema import UsersAdressesBase
from users_adresses.repository import UsersAdressesRepository
from located.repository import LocatedRepository
from code_postal.schema import CodePostalBase
from code_postal.repository import CodePostalRepository
from located.router import get_located_by_ids

def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close_all()

router = APIRouter(tags=["users"])

models.Base.metadata.create_all(bind=engine)

db_dependency= Annotated[Session, Depends(get_db)]

@router.get("/users/{user_id}", response_model=UserBase)
async def get_user( user_id: int, user_repository: UsersRepository = Depends(UsersRepository), db: Session = Depends(get_db))-> UserBase:
    user = await user_repository.get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    user_dict = model_to_dict(user) 
    return UserBase(**user_dict)

@router.get("/users", response_model=list[UserBase])
async def get_users(user_repository: UsersRepository = Depends(UsersRepository), db: Session = Depends(get_db)) -> list[UserBase]:
    users = await user_repository.get_all_users(db)
    users_dict = [model_to_dict(user) for user in users]
    return [UserBase(**user_dict) for user_dict in users_dict]

    
@router.post("/users/", response_model=UserBase)
async def create_user(user: UserBase,user_repository: UsersRepository = Depends(UsersRepository), db: Session = Depends(get_db))->UserBase:
    user_post = await user_repository.create_user(db, user)
    user_dict =model_to_dict(user_post)
    return UserBase(**user_dict)

@router.put("/users/{user_id}", response_model=UserBase)
async def update_user(user_id: int,user_data: UserBase, user_repository: UsersRepository = Depends(UsersRepository), db: Session = Depends(get_db))-> UserBase:
    user_put = await user_repository.update_user(db, user_id, user_data)
    if user_put is None:
        raise HTTPException(status_code=404, detail="User not found")
    user_dict = model_to_dict(user_put)
    return UserBase(**user_dict)

@router.post("/users/addresses/{user_id}", response_model=UsersAdressesBase)
async def create_new_user_address(user_id:int,adresse:UsersAdressesBase,code_postal:CodePostalBase,code_postal_repository:CodePostalRepository= Depends(CodePostalRepository),located_repository:LocatedRepository= Depends(LocatedRepository),user_adresse_repository: UsersAdressesRepository = Depends(UsersAdressesRepository),adresse_type_repository: AdresseTypesRepository = Depends(AdresseTypesRepository), db: Session = Depends(get_db)) -> UsersAdressesBase:
    db_address = await create_user_address(adresse,code_postal,code_postal_repository,located_repository, user_adresse_repository,db)
    adresse_type = await get_adresses_type_user(user_id,adresse_type_repository,db)
    await create_adresses_types(adresse_type,adresse_type_repository,db)
    return db_address

@router.put("/users/{adresses_id}/addresses", response_model=UsersAdressesBase)
async def modify_user_address(code_postal:int|None,user_id:int,adresses_id:int,adresse:UsersAdressesBase,adresse_type:AdresseTypeBase,located_repository:LocatedRepository= Depends(LocatedRepository),code_postal_repository:CodePostalRepository= Depends(CodePostalRepository),user_adresse_repository: UsersAdressesRepository = Depends(UsersAdressesRepository),adresse_type_repository: AdresseTypesRepository = Depends(AdresseTypesRepository), db: Session = Depends(get_db)) -> UsersAdressesBase:
    code =await get_located_by_ids(adresses_id,located_repository,db)
    print('ha')
    code_postal_unchange = code.Id_Code_Postal
    if not code_postal:
        print('hey')
        code_postal=code_postal_unchange
    db_address = await update_user_address(adresses_id,code_postal,adresse,code_postal_repository, user_adresse_repository,located_repository,db)
    print('ho')
    adresse_type = await adresse_type_repository.get_adressestypes_user(db, user_id)
    await update_adresse_type(adresse_type.Id_Adresse_Type,adresse_type,adresse_type_repository,db)
    return db_address

@router.get("/users/{user_id}/addresses", response_model=list[UsersAdressesBase])
async def retrieve_user_address(user_id:int,user_adresse_repository: UsersAdressesRepository = Depends(UsersAdressesRepository),adresse_type_repository: AdresseTypesRepository = Depends(AdresseTypesRepository), db: Session = Depends(get_db)) -> list[UsersAdressesBase]:
    adresse_type = await get_adresses_type_user(user_id,adresse_type_repository,db)
    db_address = await get_user_addresses(adresse_type.Id_Users_adresses, user_adresse_repository,db)
    return db_address

@router.post("/users/{user_id}/addresses", response_model=AdresseTypeBase)
async def create_address_type_for_user(adresse_type:AdresseTypeBase,user_adresse_repository: UsersAdressesRepository = Depends(UsersAdressesRepository),db: Session = Depends(get_db)) -> AdresseTypeBase:
    db_address = await create_adresses_types(adresse_type, user_adresse_repository,db)
    return db_address

@router.put("/users/{adresse_id}/addresses", response_model=list[UsersAdressesBase])
async def update_user_adresse_type(adresse_id:int,adresse_type:AdresseTypeBase,user_adresse_repository: UsersAdressesRepository = Depends(UsersAdressesRepository),adresse_type_repository: AdresseTypesRepository = Depends(AdresseTypesRepository), db: Session = Depends(get_db)) -> list[UsersAdressesBase]:
    db_address = await update_adresse_type(adresse_id,adresse_type ,user_adresse_repository,db)
    return db_address