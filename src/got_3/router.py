import season.models as models
import main as get_db
from typing import Annotated
from .schema import GotBase
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from database import engine, SessionLocal
from .repository import GotRepository
from common import model_to_dict

def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close_all()

router = APIRouter(tags=["got"])

models.Base.metadata.create_all(bind=engine)

db_dependency= Annotated[Session, Depends(get_db)]

@router.get("/got/", status_code=status.HTTP_200_OK, response_model=list[GotBase])
async def get_gots(got_repository: GotRepository = Depends(GotRepository), db: Session = Depends(get_db)) -> list[GotBase]:
    gots = await got_repository.get_got(db)
    gots_list = [model_to_dict(got) for got in gots]
    return [GotBase(**got_dict) for got_dict in gots_list]

@router.get("/got/{got_id}", status_code=status.HTTP_200_OK, response_model=GotBase)
async def get_got_by_id(got_id: int, got_repository: GotRepository = Depends(GotRepository), db: Session = Depends(get_db)) -> GotBase:
    got = await got_repository.get_got_by_id(db, got_id)
    if got is None:
        raise HTTPException(status_code=404, detail="got not found")
    return GotBase(**model_to_dict(got))

@router.post("/got/", status_code=status.HTTP_201_CREATED, response_model=GotBase)
async def create_got(got: GotBase, got_repository: GotRepository = Depends(GotRepository), db: Session = Depends(get_db)) -> GotBase:
    new_got = await got_repository.create_got(db, got)
    got_dict = model_to_dict(new_got)
    return GotBase(**got_dict)

@router.put("/got/{got_id}", status_code=status.HTTP_200_OK, response_model=GotBase)
async def update_got(got_id: int, got: GotBase, got_repository: GotRepository = Depends(GotRepository), db: Session = Depends(get_db)) -> GotBase:
    updated_got = await got_repository.update_got(db, got_id, got)
    if updated_got is None:
        raise HTTPException(status_code=404, detail="got not found")
    got_dict = model_to_dict(updated_got)
    return GotBase(**got_dict)
