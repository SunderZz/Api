import season.models as models
import main as get_db
from typing import Annotated
from .schema import GivenBase
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from database import engine, SessionLocal
from .repository import GivenRepository
from common import model_to_dict

def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close_all()

router = APIRouter(tags=["given"])

models.Base.metadata.create_all(bind=engine)

db_dependency= Annotated[Session, Depends(get_db)]

@router.get("/given/", status_code=status.HTTP_200_OK, response_model=list[GivenBase])
async def get_givens(given_repository: GivenRepository = Depends(GivenRepository), db: Session = Depends(get_db)) -> list[GivenBase]:
    givens = await given_repository.get_given(db)
    givens_list = [model_to_dict(given) for given in givens]
    return [GivenBase(**given_dict) for given_dict in givens_list]

@router.get("/given/{given_id}", status_code=status.HTTP_200_OK, response_model=GivenBase)
async def get_given_by_id(given_id: int, given_repository: GivenRepository = Depends(GivenRepository), db: Session = Depends(get_db)) -> GivenBase:
    given = await given_repository.get_given_by_id(db, given_id)
    if given is None:
        raise HTTPException(status_code=404, detail="given not found")
    return GivenBase(**model_to_dict(given))

@router.post("/given/", status_code=status.HTTP_201_CREATED, response_model=GivenBase)
async def create_given(given: GivenBase, given_repository: GivenRepository = Depends(GivenRepository), db: Session = Depends(get_db)) -> GivenBase:
    new_given = await given_repository.create_given(db, given)
    given_dict = model_to_dict(new_given)
    return GivenBase(**given_dict)

@router.put("/given/{given_id}", status_code=status.HTTP_200_OK, response_model=GivenBase)
async def update_given(given_id: int, given: GivenBase, given_repository: GivenRepository = Depends(GivenRepository), db: Session = Depends(get_db)) -> GivenBase:
    updated_given = await given_repository.update_given(db, given_id, given)
    if updated_given is None:
        raise HTTPException(status_code=404, detail="given not found")
    given_dict = model_to_dict(updated_given)
    return GivenBase(**given_dict)
