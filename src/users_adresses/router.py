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


@router.get("/users/{user_id}/addresses", response_model=list[UsersAdressesBase])
async def get_user_addresses(user_id: int, db: Session = Depends(get_db))->list[UsersAdressesBase]:
    adresses = await UsersAdressesRepository.get_user_addresses(db, user_id)
    if not adresses:
        raise HTTPException(status_code=404, detail="addresses not found")
    addresses_dict = [model_to_dict(adresse) for adresse in adresses]
    return [UsersAdressesBase(**adresse_dict) for adresse_dict in addresses_dict]


@router.post("/users_adresses/{user_id}/addresses", response_model=UsersAdressesBase)
async def create_user_address(user_id: int, address: UsersAdressesBase, db: Session = Depends(get_db)) -> UsersAdressesBase:
    db_address = await UsersAdressesRepository.create_user_address(db, user_id, address)
    address_dict = model_to_dict(db_address) 
    return UsersAdressesBase(**address_dict)


@router.put("/users/{user_id}/addresses/{address_id}", response_model=UsersAdressesBase)
async def update_user_address(address_id: int, address: UsersAdressesBase, db: Session = Depends(get_db)) -> UsersAdressesBase:
    updated_address = await UsersAdressesRepository.update_user_address(db, address_id, address)
    address_dict = model_to_dict(updated_address)
    return UsersAdressesBase(**address_dict)
