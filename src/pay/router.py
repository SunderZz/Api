import pay.models as models
from typing import Annotated
from.schema import PayBase
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
import main as get_db
from database import engine, SessionLocal
from.repository import PayRepository
from common import model_to_dict

def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close_all()

router = APIRouter(tags=["pay"])

models.Base.metadata.create_all(bind=engine)

db_dependency= Annotated[Session, Depends(get_db)]

@router.get("/pay/", status_code=status.HTTP_200_OK, response_model=list[PayBase])
async def get_pays(pay_repository: PayRepository = Depends(PayRepository), db: Session = Depends(get_db)) -> list[PayBase]:
    pays = await pay_repository.get_pays(db)
    pays_list = [model_to_dict(pay) for pay in pays]
    return [PayBase(**pay_dict) for pay_dict in pays_list]

@router.get("/pay/{payment_id}", status_code=status.HTTP_200_OK, response_model=PayBase)
async def get_pay_by_id(payment_id: int, pay_repository: PayRepository = Depends(PayRepository), db: Session = Depends(get_db)) -> PayBase:
    pay = await pay_repository.get_pay_by_id(db, payment_id)
    if pay is None:
        raise HTTPException(status_code=404, detail="Pay not found")
    return PayBase(**model_to_dict(pay))

@router.post("/pay/", status_code=status.HTTP_201_CREATED, response_model=PayBase)
async def create_pay(pay: PayBase, pay_repository: PayRepository = Depends(PayRepository), db: Session = Depends(get_db)) -> PayBase:
    new_pay = await pay_repository.create_pay(db, pay)
    pay_dict = model_to_dict(new_pay)
    return PayBase(**pay_dict)

@router.put("/pay/{payment_id}", status_code=status.HTTP_200_OK, response_model=PayBase)
async def update_pay(payment_id: int, pay: PayBase, pay_repository: PayRepository = Depends(PayRepository), db: Session = Depends(get_db)) -> PayBase:
    updated_pay = await pay_repository.update_pay(db, payment_id, pay)
    if updated_pay is None:
        raise HTTPException(status_code=404, detail="Pay not found")
    pay_dict = model_to_dict(updated_pay)
    return PayBase(**pay_dict)
