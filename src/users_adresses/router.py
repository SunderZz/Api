from datetime import datetime
from http.client import HTTPException
import users_adresses.models as models
import main as get_db
from typing import Annotated
from .schema import UsersAdressesBase, UsersAdressesInDB
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import engine, SessionLocal
from .repository import UsersAdressesRepository


def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close_all()

router = APIRouter(tags=["users_adresses"])

models.Base.metadata.create_all(bind=engine)

db_dependency= Annotated[Session, Depends(get_db)]


@router.get("users_adresses/{user_id}", response_model=UsersAdressesInDB, summary="get users adresses")
def read_users_adresses(user_id: int, db: Session = Depends(get_db), repository= UsersAdressesRepository):
    db_user_adresses = repository.get_users_adresses(db, user_id)
    if db_user_adresses is None:
        raise HTTPException(status_code=404, detail="User address not found")
    return db_user_adresses


@router.post("/users/{user_id}/address")
def create_user_address(users_id: int, user_address: UsersAdressesBase, db: Session = Depends(get_db)):
    db_user = db.query(models.Users_adresses).filter(models.Users_adresses.Id_Users_adresses == users_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    db_user_address = models.Users_adresses(**user_address.dict(), user_id=users_id)
    db.add(db_user_address)
    db.commit()
    db.refresh(db_user_address)
    return db_user_address

@router.put("/user/{user_id}/address")
def update_user_address(user_id: int, address: UsersAdressesBase, db: Session = Depends(get_db)):
    user_address = db.query(models.Users_adresses).filter(models.Users_adresses.Id_Users_adresses == user_id).first()
    if user_address is None:
        raise HTTPException(status_code=404, detail="User not found")
    user_address.adresse = address.adresse
    user_address.modification = datetime.now()
    db.commit()
    return user_address
# get user_adresse ( with id)
# post user adresse (with id)
# put user adresse ( with id)