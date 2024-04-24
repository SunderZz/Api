import users.models as models
from typing import Annotated
from .schema import PreferenceshipBase
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

router = APIRouter(tags=["preference_ship"])

models.Base.metadata.create_all(bind=engine)

db_dependency= Annotated[Session, Depends(get_db)]


@router.post("/preference_ship/", status_code= status.HTTP_201_CREATED)
async def create_user(preferenceship:PreferenceshipBase, db: db_dependency):
    db_user= models(**preferenceship.model_dump())
    db.add(db_user)
    db.commit()

#get preference_ship based on id order
#put preference_ship
#post preference_ship
