import users.models as models
from typing import Annotated
from .schema import CustomersBase
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
import main as get_db
from database import engine, SessionLocal
from common import model_to_dict
from .repository import CustomersRepository

def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close_all()

router = APIRouter(tags=["customers"])

models.Base.metadata.create_all(bind=engine)

db_dependency= Annotated[Session, Depends(get_db)]


@router.get("/customers/", status_code=status.HTTP_200_OK, response_model=list[CustomersBase])
async def get_customers(customers_repository: CustomersRepository = Depends(CustomersRepository),db: Session = Depends(get_db))-> list[CustomersBase]:
    customers = await customers_repository.get_customers(db)
    customers_list = [model_to_dict(customer) for customer in customers]
    return [CustomersBase(**customers_dict) for customers_dict in customers_list]


@router.get("/customers/{customers}", response_model=CustomersBase)
async def get_customer_value(customers: str, customers_repository: CustomersRepository = Depends(CustomersRepository), db: Session = Depends(get_db)) -> CustomersBase:
    value = await customers_repository.get_customers_query(db, customers)
    if value is None:
        raise HTTPException(status_code=404, detail="customer not found or attribute not found")
    customers_dict = model_to_dict(value)
        
    return CustomersBase(**customers_dict)


@router.post("/customers/", status_code=status.HTTP_201_CREATED, response_model=CustomersBase)
async def create_customer(customer: CustomersBase,customers_repository: CustomersRepository = Depends(CustomersRepository), db: Session = Depends(get_db))-> CustomersBase:
    new_customer = await customers_repository.create_customers(db, customer)
    customers_dict = model_to_dict(new_customer) 
    return CustomersBase(**customers_dict)

@router.put("/customers/{customer_id}", status_code=status.HTTP_200_OK, response_model=CustomersBase)
async def update_customer(customer_id: int, customer: CustomersBase,customer_repository: CustomersRepository = Depends(CustomersRepository), db: Session = Depends(get_db))-> CustomersBase:
    updated_customer = await customer_repository.update_customers(db, customer_id, customer)
    if updated_customer is None:
        raise HTTPException(status_code=404, detail="customers not found")
    customer_dict = model_to_dict(updated_customer) 
    return CustomersBase(**customer_dict)