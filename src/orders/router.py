import users.models as models
from typing import Annotated
from .schema import OrdersBase
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
import main as get_db
from database import engine, SessionLocal
from .repository import OrdersRepository
from common import model_to_dict

def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close_all()

router = APIRouter(tags=["orders"])

models.Base.metadata.create_all(bind=engine)

db_dependency= Annotated[Session, Depends(get_db)]


@router.get("/orders/", status_code=status.HTTP_200_OK, response_model=list[OrdersBase])
async def get_orderss(orders_repository: OrdersRepository = Depends(OrdersRepository),db: Session = Depends(get_db))-> list[OrdersBase]:
    orderss = await orders_repository.get_orders(db)
    orders_list = [model_to_dict(orders) for orders in orderss]
    return [OrdersBase(**orders_dict) for orders_dict in orders_list]


@router.get("/orders/{orders}", response_model=OrdersBase)
async def get_orders_value(orders: str, orders_repository: OrdersRepository = Depends(OrdersRepository), db: Session = Depends(get_db)) -> OrdersBase:
    value = await orders_repository.get_orders_query(db, orders)
    if value is None:
        raise HTTPException(status_code=404, detail="orders not found or attribute not found")
    return OrdersBase(value=value)


@router.post("/orders/", status_code=status.HTTP_201_CREATED, response_model=OrdersBase)
async def create_orders(orders: OrdersBase,orders_repository: OrdersRepository = Depends(OrdersRepository), db: Session = Depends(get_db))-> OrdersBase:
    new_orders = await orders_repository.create_orders(db, orders)
    orders_dict = model_to_dict(new_orders) 
    return OrdersBase(**orders_dict)

@router.put("/orders/{orders_id}", status_code=status.HTTP_200_OK, response_model=OrdersBase)
async def update_orders(orders_id: int, orders: OrdersBase,orders_repository: OrdersRepository = Depends(OrdersRepository), db: Session = Depends(get_db))-> OrdersBase:
    updated_orders = await orders_repository.update_orders(db, orders_id, orders)
    if updated_orders is None:
        raise HTTPException(status_code=404, detail="orders not found")
    orders_dict = model_to_dict(updated_orders) 
    return OrdersBase(**orders_dict)