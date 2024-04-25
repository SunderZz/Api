import tva.models as models
from typing import Annotated
from .schema import TvaBase, TvaCalculationResult
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import main as get_db
from database import engine, SessionLocal
from .repository import TvaRepository
from common import model_to_dict

def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close_all()

router = APIRouter(tags=["tva"])

models.Base.metadata.create_all(bind=engine)

db_dependency= Annotated[Session, Depends(get_db)]


@router.get("/tva/{tva_id}", response_model=TvaBase)
async def get_tva(tva_id: int, tva_repository: TvaRepository = Depends(TvaRepository), db: Session = Depends(get_db))->TvaBase:
    tva = await tva_repository.get_tva(db, tva_id)
    if tva is None:
        raise HTTPException(status_code=404, detail="Tva not found")
    tva_dict = model_to_dict(tva) 
    return TvaBase(**tva_dict)

@router.get("/tva/calculate/{tva_name}", response_model=TvaCalculationResult)
async def calculate_tva(tva_name: str, price: float, db: Session = Depends(get_db), tva_repository: TvaRepository = Depends(TvaRepository))->TvaCalculationResult:
    tva_value = await tva_repository.calculate_tva(db, price, tva_name)
    if tva_value is None:
        raise HTTPException(status_code=404, detail="Tva not found")
    return TvaCalculationResult(value=tva_value)

@router.put("/tva/{tva_id}", response_model=TvaBase)
async def update_tva(tva_id: int, tva: TvaBase,  tva_repository: TvaRepository = Depends(TvaRepository), db: Session = Depends(get_db))->TvaBase:
    updated_tva = await tva_repository.update_tva(db, tva, tva_id)
    if updated_tva is None:
        raise HTTPException(status_code=404, detail="Tva not found")
    tva_dict = model_to_dict(updated_tva) 
    return TvaBase(**tva_dict)

@router.post("/tva/", response_model=TvaBase)
async def create_tva(tva: TvaBase, tva_repository: TvaRepository = Depends(TvaRepository), db: Session = Depends(get_db))->TvaBase:
    created_tva = await tva_repository.create_tva(db, tva)
    tva_dict = model_to_dict(created_tva) 
    return TvaBase(**tva_dict)
