from fastapi import HTTPException
import users_adresses.models as models
import main as get_db
from typing import Annotated
from .schema import UsersAdressesBase
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import engine, SessionLocal
from .repository import UsersAdressesRepository
from common import model_to_dict

from located.router import create_located,update_located,get_located_by_ids
from located.schema import LocatedBase
from located.repository import LocatedRepository
from code_postal.router import create_code_postal,update_code_postal,get_code_postal_value
from code_postal.schema import CodePostalBase,CodePostalIdBase
from code_postal.repository import CodePostalRepository

def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close_all()

router = APIRouter(tags=["users_adresses"])

models.Base.metadata.create_all(bind=engine)

db_dependency= Annotated[Session, Depends(get_db)]


@router.get("/users/{adresse_id}/addresses", response_model=list[UsersAdressesBase])
async def get_user_addresses(adresse_id: int,user_adresse_repository: UsersAdressesRepository = Depends(UsersAdressesRepository), db: Session = Depends(get_db))->list[UsersAdressesBase]:
    adresses = await user_adresse_repository.get_user_addresses(db, adresse_id)
    if not adresses:
        raise HTTPException(status_code=404, detail="addresses not found")
    addresses_dict = [model_to_dict(adresse) for adresse in adresses]
    return [UsersAdressesBase(**adresse_dict) for adresse_dict in addresses_dict]


@router.post("/users_adresses/addresses", response_model=UsersAdressesBase)
async def create_user_address(address: UsersAdressesBase,code_postal:CodePostalBase,code_postal_repository:CodePostalRepository= Depends(CodePostalRepository),located_repository:LocatedRepository= Depends(LocatedRepository),user_adresse_repository: UsersAdressesRepository = Depends(UsersAdressesRepository), db: Session = Depends(get_db)) -> UsersAdressesBase:
    db_address = await user_adresse_repository.create_user_address(db, address)
    code =await create_code_postal(code_postal,code_postal_repository,db)
    value = await get_code_postal_value(code.code_postal,code_postal_repository,db)
    await create_located(LocatedBase(Id_Code_Postal=value.Id_Code_Postal,Id_Users_adresses=db_address.Id_Users_adresses),located_repository,db)
    address_dict = model_to_dict(db_address) 
    return UsersAdressesBase(**address_dict)


@router.put("/users/{user_id}/addresses/{address_id}", response_model=UsersAdressesBase)
async def update_user_address(address_id: int,postal_code:int,address: UsersAdressesBase,code_postal_repository:CodePostalRepository= Depends(CodePostalRepository),user_adresse_repository: UsersAdressesRepository = Depends(UsersAdressesRepository),located_repository:LocatedRepository= Depends(LocatedRepository), db: Session = Depends(get_db)) -> UsersAdressesBase:
    updated_address = await user_adresse_repository.update_user_address(db, address_id, address)
    await get_located_by_ids(updated_address.Id_Users_adresses,located_repository,db)
    code =await create_code_postal(CodePostalBase(code_postal=postal_code),code_postal_repository,db)
    value = await get_code_postal_value(code.code_postal,code_postal_repository,db)
    await update_located(updated_address.Id_Users_adresses,LocatedBase(Id_Code_Postal=value.Id_Code_Postal,Id_Users_adresses=updated_address.Id_Users_adresses),located_repository,db)
    address_dict = model_to_dict(updated_address)
    return UsersAdressesBase(**address_dict)
