import users.models as models
from typing import Annotated
from .schema import Casual5Base
from fastapi import APIRouter, FastAPI, Depends, status
from sqlalchemy.orm import Session
import main as get_db
from database import engine, SessionLocal


def get_db():
    db = SessionLocal
    try: 
        yield db
    finally:
        db.close_all()

router = APIRouter(tags=["casual"])

models.Base.metadata.create_all(bind=engine)

db_dependency= Annotated[Session, Depends(get_db)]


@router.post("/casual/", status_code= status.HTTP_201_CREATED)
async def create_user(casual:Casual5Base, db: db_dependency):
    db_user= models(**casual.model_dump())
    db.add(db_user)
    db.commit()