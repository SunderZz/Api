import users.models as models
from typing import Annotated
from .schema import UserBase
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

router = APIRouter(tags=["recipes"])

models.Base.metadata.create_all(bind=engine)

db_dependency= Annotated[Session, Depends(get_db)]


@router.get("/recipes/", status_code= status.HTTP_200_OK)
async def get_recipes(user:UserBase, db: db_dependency):
    db_user= models(**user.model_dump())
    db.add(db_user)
    db.commit()