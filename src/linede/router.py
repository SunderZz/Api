import season.models as models
import main as get_db
from typing import Annotated
from .schema import LinedeBase
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from database import engine, SessionLocal
from .repository import LinedeRepository
from common import model_to_dict

def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close_all()

router = APIRouter(tags=["linede"])

models.Base.metadata.create_all(bind=engine)

db_dependency= Annotated[Session, Depends(get_db)]

@router.get("/linede/", status_code=status.HTTP_200_OK, response_model=list[LinedeBase])
async def get_linedes(linede_repository: LinedeRepository = Depends(LinedeRepository), db: Session = Depends(get_db)) -> list[LinedeBase]:
    linedes = await linede_repository.get_linede(db)
    linedes_list = [model_to_dict(linede) for linede in linedes]
    return [LinedeBase(**linede_dict) for linede_dict in linedes_list]

@router.get("/linede/{linede_id}", status_code=status.HTTP_200_OK, response_model=LinedeBase)
async def get_linede_by_id(linede_id: int, linede_repository: LinedeRepository = Depends(LinedeRepository), db: Session = Depends(get_db)) -> LinedeBase:
    linede = await linede_repository.get_linede_by_id(db, linede_id)
    if linede is None:
        raise HTTPException(status_code=404, detail="linede not found")
    return LinedeBase(**model_to_dict(linede))

@router.post("/linede/", status_code=status.HTTP_201_CREATED, response_model=LinedeBase)
async def create_linede(linede: LinedeBase, linede_repository: LinedeRepository = Depends(LinedeRepository), db: Session = Depends(get_db)) -> LinedeBase:
    new_linede = await linede_repository.create_linede(db, linede)
    linede_dict = model_to_dict(new_linede)
    return LinedeBase(**linede_dict)

@router.put("/linede/{linede_id}", status_code=status.HTTP_200_OK, response_model=LinedeBase)
async def update_linede(linede_id: int, linede: LinedeBase, linede_repository: LinedeRepository = Depends(LinedeRepository), db: Session = Depends(get_db)) -> LinedeBase:
    updated_linede = await linede_repository.update_linede(db, linede_id, linede)
    if updated_linede is None:
        raise HTTPException(status_code=404, detail="linede not found")
    linede_dict = model_to_dict(updated_linede)
    return LinedeBase(**linede_dict)
