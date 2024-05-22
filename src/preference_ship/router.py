import users.models as models
from typing import Annotated
from .schema import PreferenceshipBase,PreferenceshipIdBase
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
import main as get_db
from database import engine, SessionLocal
from common import model_to_dict
from .repository import PreferenceshipRepository

def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close_all()

router = APIRouter(tags=["preference_ship"])

models.Base.metadata.create_all(bind=engine)

db_dependency= Annotated[Session, Depends(get_db)]


@router.post("/preferenceship/", status_code=status.HTTP_201_CREATED, response_model=PreferenceshipBase)
async def get_preferenceship(preferenceship: PreferenceshipBase,preferenceship_repository: PreferenceshipRepository = Depends(PreferenceshipRepository), db: Session = Depends(get_db))-> PreferenceshipBase:
    new_preferenceship = await preferenceship_repository.create_preferenceship(db, preferenceship)
    preferenceship_dict = model_to_dict(new_preferenceship) 
    return PreferenceshipBase(**preferenceship_dict)

@router.put("/preferenceship/{product_id}", status_code=status.HTTP_200_OK, response_model=PreferenceshipBase)
async def update_preferenceship(preferenceship_id: int, preferenceship: PreferenceshipBase,product_repository: PreferenceshipRepository = Depends(PreferenceshipRepository), db: Session = Depends(get_db))-> PreferenceshipBase:
    updated_preferenceship = await product_repository.update_preferenceship(db, preferenceship_id, preferenceship)
    if updated_preferenceship is None:
        raise HTTPException(status_code=404, detail="produit_image not found")
    preferenceship_image_dict = model_to_dict(updated_preferenceship) 
    return PreferenceshipBase(**preferenceship_image_dict)
    

@router.post("/preference_ship/", status_code=status.HTTP_201_CREATED, response_model=PreferenceshipIdBase)
async def create_preference_ship(preference_ship: PreferenceshipBase,preference_ship_repository: PreferenceshipRepository = Depends(PreferenceshipRepository), db: Session = Depends(get_db))-> PreferenceshipIdBase:
    new_preference_ship = await preference_ship_repository.create_preferenceship(db, preference_ship)
    preference_ship_dict = model_to_dict(new_preference_ship) 
    return PreferenceshipIdBase(**preference_ship_dict)
