import redac.models as models
from typing import Annotated
from.schema import RedactBase
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
import main as get_db
from database import engine, SessionLocal
from.repository import RedactRepository
from common import model_to_dict

def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close_all()

router = APIRouter(tags=["redact"])

models.Base.metadata.create_all(bind=engine)

db_dependency = Annotated[Session, Depends(get_db)]

@router.get("/redact/", status_code=status.HTTP_200_OK, response_model=list[RedactBase])
async def get_redacts(redact_repository: RedactRepository = Depends(RedactRepository), db: Session = Depends(get_db)) -> list[RedactBase]:
    redacts = await redact_repository.get_Redact(db)
    redacts_list = [model_to_dict(redact) for redact in redacts]
    return [RedactBase(**redact_dict) for redact_dict in redacts_list]

@router.get("/redact/{redact_id}", response_model=RedactBase)
async def get_redact_value(admin_id:int, redact_id: int, redact_repository: RedactRepository = Depends(RedactRepository), db: Session = Depends(get_db)) -> RedactBase:
    value = await redact_repository.get_Redact_by_admin_and_recipe(db,admin_id, redact_id)
    if value is None:
        raise HTTPException(status_code=404, detail="redact not found")
    redact_dict = model_to_dict(value) 
    return RedactBase(**redact_dict)

@router.post("/redact/", status_code=status.HTTP_201_CREATED, response_model=RedactBase)
async def create_redact(admin_id:int,redact_id:int,redact: RedactBase, redact_repository: RedactRepository = Depends(RedactRepository), db: Session = Depends(get_db)) -> RedactBase:
    existing_redac  = await redact_repository.get_Redact_by_admin_and_recipe(db,admin_id,redact_id)
    if existing_redac:
        return existing_redac
    new_redact = await redact_repository.create_Redact(db, redact)
    redact_dict = model_to_dict(new_redact) 
    return RedactBase(**redact_dict)

@router.put("/redact/{admin_id}/{recipe_id}", status_code=status.HTTP_200_OK, response_model=RedactBase)
async def update_redact(admin_id: int, recipe_id: int, redact: RedactBase, redact_repository: RedactRepository = Depends(RedactRepository), db: Session = Depends(get_db)) -> RedactBase:
    updated_redact = await redact_repository.update_Redact(db, admin_id, recipe_id, redact)
    if updated_redact is None:
        raise HTTPException(status_code=404, detail="redact not found")
    redact_dict = model_to_dict(updated_redact) 
    return RedactBase(**redact_dict)
