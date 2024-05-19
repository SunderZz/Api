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
async def create_user_address(address: UsersAdressesBase,user_adresse_repository: UsersAdressesRepository = Depends(UsersAdressesRepository), db: Session = Depends(get_db)) -> UsersAdressesBase:
    db_address = await user_adresse_repository.create_user_address(db, address)
    address_dict = model_to_dict(db_address) 
    return UsersAdressesBase(**address_dict)


@router.put("/users/{user_id}/addresses/{address_id}", response_model=UsersAdressesBase)
async def update_user_address(address_id: int, address: UsersAdressesBase,user_adresse_repository: UsersAdressesRepository = Depends(UsersAdressesRepository), db: Session = Depends(get_db)) -> UsersAdressesBase:
    updated_address = await user_adresse_repository.update_user_address(db, address_id, address)
    address_dict = model_to_dict(updated_address)
    return UsersAdressesBase(**address_dict)
