import users.models as models
from typing import Annotated
from .schema import UsersAdressesBase
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
import main as get_db
from database import engine, SessionLocal


def get_db():
    db = SessionLocal
    try: 
        yield db
    finally:
        db.close_all()

router = APIRouter(tags=["users_adresses"])

models.Base.metadata.create_all(bind=engine)

db_dependency= Annotated[Session, Depends(get_db)]


@router.get("/users_adresses/", status_code= status.HTTP_200_OK)
async def create_user(user_adresses:UsersAdressesBase, db: db_dependency):
    db_user= models(**user_adresses.model_dump())
    db.add(db_user)
    db.commit()