import users.models as models
from typing import Annotated
from .schema import AdresseTypeBase
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
import main as get_db
from database import engine, SessionLocal
from common import model_to_dict
from .repository import AdresseTypesRepository

def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close_all()

router = APIRouter(tags=["adresse_types"])

models.Base.metadata.create_all(bind=engine)

db_dependency= Annotated[Session, Depends(get_db)]

@router.get("/adresses_types/", status_code=status.HTTP_200_OK, response_model=list[AdresseTypeBase])
async def get_adresses_types(adresses_types_repository: AdresseTypesRepository = Depends(AdresseTypesRepository),db: Session = Depends(get_db))-> list[AdresseTypeBase]:
    adresses_types = await adresses_types_repository.get_adressestypes(db)
    adresses_types_list = [model_to_dict(adresses_type) for adresses_type in adresses_types]
    return [AdresseTypeBase(**adresses_type_dict) for adresses_type_dict in adresses_types_list]


@router.get("/adresses_types/{adresses_types}", response_model=AdresseTypeBase)
async def get_adresses_type_value(adresses_types: str, adresses_types_repository: AdresseTypesRepository = Depends(AdresseTypesRepository), db: Session = Depends(get_db)) -> AdresseTypeBase:
    value = await adresses_types_repository.get_adressestypes_query(db, adresses_types)
    if value is None:
        raise HTTPException(status_code=404, detail="adresses_type not found or attribute not found")
    adresses_type_dict = model_to_dict(value)
        
    return AdresseTypeBase(**adresses_type_dict)


@router.post("/adresses_types/", status_code=status.HTTP_201_CREATED, response_model=AdresseTypeBase)
async def create_producer(producer: AdresseTypeBase,adresses_types_repository: AdresseTypesRepository = Depends(AdresseTypesRepository), db: Session = Depends(get_db))-> AdresseTypeBase:
    new_producer = await adresses_types_repository.create_adressestypes(db, producer)
    adresses_type_dict = model_to_dict(new_producer) 
    return AdresseTypeBase(**adresses_type_dict)

@router.put("/adresses_types/{adresses_type_id}", status_code=status.HTTP_200_OK, response_model=AdresseTypeBase)
async def update_producer(adresses_type_id: int, producer: AdresseTypeBase,adresses_type_repository: AdresseTypesRepository = Depends(AdresseTypesRepository), db: Session = Depends(get_db))-> AdresseTypeBase:
    updated_producer = await adresses_type_repository.update_adressestypes(db, adresses_type_id, producer)
    if updated_producer is None:
        raise HTTPException(status_code=404, detail="produit_image not found")
    produit_image_dict = model_to_dict(updated_producer) 
    return AdresseTypeBase(**produit_image_dict)