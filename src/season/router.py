# import season.models as models
from typing import Annotated
from .schema import SeasonBase
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

router = APIRouter(tags=["season"])

# models.Base.metadata.create_all(bind=engine)

db_dependency= Annotated[Session, Depends(get_db)]


# @router.get("/season/", status_code= status.HTTP_201_CREATED)
# async def get_season(db: db_dependency):
#     season= db.query(models.Season).all()
#     return {"season":season}

# @router.post("/season/", status_code= status.HTTP_201_CREATED)
# async def get_season(db: db_dependency):
#     season= db.query(models.Season).all()
#     return {"season":season}