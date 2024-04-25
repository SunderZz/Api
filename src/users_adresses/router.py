from datetime import datetime
from fastapi import HTTPException
import users_adresses.models as models
import main as get_db
from typing import Annotated
from .schema import UsersAdressesBase, UsersAdressesInDB
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
def get_user_addresses(user_id: int, db: Session = Depends(get_db))->list[UsersAdressesBase]:
    addresses = UsersAdressesRepository.get_user_addresses(db, user_id)
    if not addresses:
        raise HTTPException(status_code=404, detail="User addresses not found")
    addresses_dict = [model_to_dict(address) for address in addresses]
    return [UsersAdressesBase(**address_dict) for address_dict in addresses_dict]


@router.post("/users_adresses/{user_id}/addresses", response_model=UsersAdressesBase)
def create_user_address(user_id: int, address: UsersAdressesBase, db: Session = Depends(get_db)) -> UsersAdressesBase:
    db_address = UsersAdressesRepository.create_user_address(db, user_id, address)
    address_dict = model_to_dict(db_address) 
    return UsersAdressesBase(**address_dict)


@router.put("/users/{user_id}/addresses/{address_id}", response_model=UsersAdressesBase)
def update_user_address(address_id: int, address: UsersAdressesBase, db: Session = Depends(get_db)) -> UsersAdressesBase:
    updated_address = UsersAdressesRepository.update_user_address(db, address_id, address)
    address_dict = model_to_dict(updated_address)
    return UsersAdressesBase(**address_dict)
