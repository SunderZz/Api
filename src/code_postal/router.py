import users.models as models
from typing import Annotated
from .schema import CodePostalBase
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

router = APIRouter(tags=["code_postal"])

models.Base.metadata.create_all(bind=engine)

db_dependency= Annotated[Session, Depends(get_db)]


@router.post("/code_postal/", status_code= status.HTTP_201_CREATED)
async def create_user(code:CodePostalBase, db: db_dependency):
    db_user= models(**code.model_dump())
    db.add(db_user)
    db.commit()