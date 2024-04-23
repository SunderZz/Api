import unit.models as models
from typing import Annotated
from .schema import UnitBase
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
import main as get_db
from database import engine, SessionLocal


def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close_all()

router = APIRouter(tags=["unit"])

models.Base.metadata.create_all(bind=engine)

db_dependency= Annotated[Session, Depends(get_db)]


@router.get("/unit/", status_code= status.HTTP_201_CREATED)
async def get_users(db: db_dependency):
    unit= db.query(models.Unit).all()
    return {"unit":unit}

@router.put("/unit/", status_code= status.HTTP_201_CREATED)
async def get_users(db: db_dependency):
    unit= db.query(models.Unit).all()
    return {"unit":unit}