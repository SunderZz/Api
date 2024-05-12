import season.models as models
import main as get_db
from typing import Annotated
from .schema import ManageBase
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from database import engine, SessionLocal
from .repository import ManageRepository
from common import model_to_dict

def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close_all()

router = APIRouter(tags=["manage"])

models.Base.metadata.create_all(bind=engine)

db_dependency= Annotated[Session, Depends(get_db)]

@router.get("/manage/", status_code=status.HTTP_200_OK, response_model=list[ManageBase])
async def get_manages(manage_repository: ManageRepository = Depends(ManageRepository), db: Session = Depends(get_db)) -> list[ManageBase]:
    manages = await manage_repository.get_manage(db)
    manages_list = [model_to_dict(manage) for manage in manages]
    return [ManageBase(**manage_dict) for manage_dict in manages_list]

@router.get("/manage/{manage_id}", status_code=status.HTTP_200_OK, response_model=ManageBase)
async def get_manage_by_id(manage_id: int, manage_repository: ManageRepository = Depends(ManageRepository), db: Session = Depends(get_db)) -> ManageBase:
    manage = await manage_repository.get_manage_by_id(db, manage_id)
    if manage is None:
        raise HTTPException(status_code=404, detail="manage not found")
    return ManageBase(**model_to_dict(manage))

@router.post("/manage/", status_code=status.HTTP_201_CREATED, response_model=ManageBase)
async def create_manage(manage: ManageBase, manage_repository: ManageRepository = Depends(ManageRepository), db: Session = Depends(get_db)) -> ManageBase:
    new_manage = await manage_repository.create_manage(db, manage)
    manage_dict = model_to_dict(new_manage)
    return ManageBase(**manage_dict)

@router.put("/manage/{manage_id}", status_code=status.HTTP_200_OK, response_model=ManageBase)
async def update_manage(manage_id: int, manage: ManageBase, manage_repository: ManageRepository = Depends(ManageRepository), db: Session = Depends(get_db)) -> ManageBase:
    updated_manage = await manage_repository.update_manage(db, manage_id, manage)
    if updated_manage is None:
        raise HTTPException(status_code=404, detail="manage not found")
    manage_dict = model_to_dict(updated_manage)
    return ManageBase(**manage_dict)
