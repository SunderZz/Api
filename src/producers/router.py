import users.models as models
from typing import Annotated
from .schema import ProducersBase
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
import main as get_db
from database import engine, SessionLocal
from common import model_to_dict
from .repository import ProducersRepository

def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close_all()

router = APIRouter(tags=["producers"])

models.Base.metadata.create_all(bind=engine)

db_dependency= Annotated[Session, Depends(get_db)]

@router.get("/producers/", status_code=status.HTTP_200_OK, response_model=list[ProducersBase])
async def get_producers(produit_repository: ProducersRepository = Depends(ProducersRepository),db: Session = Depends(get_db))-> list[ProducersBase]:
    producers = await produit_repository.get_producers(db)
    producers_list = [model_to_dict(producer) for producer in producers]
    return [ProducersBase(**producer_dict) for producer_dict in producers_list]


@router.get("/producers/{producers}", response_model=ProducersBase)
async def get_producer_value(producers: str, producers_repository: ProducersRepository = Depends(ProducersRepository), db: Session = Depends(get_db)) -> ProducersBase:
    value = await producers_repository.get_producers_query(db, producers)
    if value is None:
        raise HTTPException(status_code=404, detail="producer not found or attribute not found")
    producer_dict = model_to_dict(value)
        
    return ProducersBase(**producer_dict)


@router.post("/producers/", status_code=status.HTTP_201_CREATED, response_model=ProducersBase)
async def create_producer(producer: ProducersBase,producers_repository: ProducersRepository = Depends(ProducersRepository), db: Session = Depends(get_db))-> ProducersBase:
    new_producer = await producers_repository.create_producers(db, producer)
    producer_dict = model_to_dict(new_producer) 
    return ProducersBase(**producer_dict)

@router.put("/producers/{producer_id}", status_code=status.HTTP_200_OK, response_model=ProducersBase)
async def update_producer(producer_id: int, producer: ProducersBase,producer_repository: ProducersRepository = Depends(ProducersRepository), db: Session = Depends(get_db))-> ProducersBase:
    updated_producer = await producer_repository.update_producers(db, producer_id, producer)
    if updated_producer is None:
        raise HTTPException(status_code=404, detail="produit_image not found")
    produit_image_dict = model_to_dict(updated_producer) 
    return ProducersBase(**produit_image_dict)