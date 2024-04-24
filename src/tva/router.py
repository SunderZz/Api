import tva.models as models
from typing import Annotated
from .schema import TvaBase
from fastapi import APIRouter, FastAPI, Depends, status
from sqlalchemy.orm import Session
import main as get_db
from database import engine, SessionLocal


def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close_all()

router = APIRouter(tags=["tva"])

models.Base.metadata.create_all(bind=engine)

db_dependency= Annotated[Session, Depends(get_db)]


@router.get("/tva/", status_code= status.HTTP_201_CREATED)
async def get_tva(db: db_dependency):
    tva= db.query(models.Tva).all()
    return {"tva":tva}

@router.put("/tva/", status_code= status.HTTP_201_CREATED)
async def put_tva(db: db_dependency):
    tva= db.query(models.Tva).all()
    return {"tva":tva}

#get tva
#get calculated tva
#put tva
#post tva