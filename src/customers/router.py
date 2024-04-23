import users.models as models
from typing import Annotated
from .schema import CustomersBase
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

router = APIRouter(tags=["customers"])

models.Base.metadata.create_all(bind=engine)

db_dependency= Annotated[Session, Depends(get_db)]


@router.post("/customers/", status_code= status.HTTP_201_CREATED)
async def create_user(customers:CustomersBase, db: db_dependency):
    db_user= models(**customers.model_dump())
    db.add(db_user)
    db.commit()