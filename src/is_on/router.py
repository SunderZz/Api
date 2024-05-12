import season.models as models
import main as get_db
from typing import Annotated
from .schema import IsOnBase
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from database import engine, SessionLocal
from .repository import IsOnRepository
from common import model_to_dict

def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close_all()

router = APIRouter(tags=["is_on"])

models.Base.metadata.create_all(bind=engine)

db_dependency= Annotated[Session, Depends(get_db)]

@router.get("/is_on/", status_code=status.HTTP_200_OK, response_model=list[IsOnBase])
async def get_is_ons(is_on_repository: IsOnRepository = Depends(IsOnRepository), db: Session = Depends(get_db)) -> list[IsOnBase]:
    is_ons = await is_on_repository.get_is_on(db)
    is_ons_list = [model_to_dict(is_on) for is_on in is_ons]
    return [IsOnBase(**is_on_dict) for is_on_dict in is_ons_list]

@router.get("/is_on/{is_on_id}", status_code=status.HTTP_200_OK, response_model=IsOnBase)
async def get_is_on_by_id(is_on_id: int, is_on_repository: IsOnRepository = Depends(IsOnRepository), db: Session = Depends(get_db)) -> IsOnBase:
    is_on = await is_on_repository.get_is_on_by_id(db, is_on_id)
    if is_on is None:
        raise HTTPException(status_code=404, detail="is_on not found")
    return IsOnBase(**model_to_dict(is_on))

@router.post("/is_on/", status_code=status.HTTP_201_CREATED, response_model=IsOnBase)
async def create_is_on(is_on: IsOnBase, is_on_repository: IsOnRepository = Depends(IsOnRepository), db: Session = Depends(get_db)) -> IsOnBase:
    new_is_on = await is_on_repository.create_is_on(db, is_on)
    is_on_dict = model_to_dict(new_is_on)
    return IsOnBase(**is_on_dict)

@router.put("/is_on/{is_on_id}", status_code=status.HTTP_200_OK, response_model=IsOnBase)
async def update_is_on(is_on_id: int, is_on: IsOnBase, is_on_repository: IsOnRepository = Depends(IsOnRepository), db: Session = Depends(get_db)) -> IsOnBase:
    updated_is_on = await is_on_repository.update_is_on(db, is_on_id, is_on)
    if updated_is_on is None:
        raise HTTPException(status_code=404, detail="is_on not found")
    is_on_dict = model_to_dict(updated_is_on)
    return IsOnBase(**is_on_dict)
