from http.client import HTTPException
import users.models as models
import main as get_db
from typing import Annotated
from .schema import UsersAdressesBase
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from database import engine, SessionLocal
from .repository import get_adress

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

@router.get("/users_adresses/{user_id}/get_user_adresses/")
def get_user_adresse_endpoint(user_id: int, new_email: str, db: Session = Depends(get_db)):
    try:
        get_adress(db, user_id, new_email)
        return {"detail": "Email updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))