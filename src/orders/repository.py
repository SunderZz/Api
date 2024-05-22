from sqlalchemy.orm import Session
from .models import Orders

class OrdersRepository:
    async def get_orders(self, db: Session)->list[Orders]:
        return db.query(Orders).all()
    
    async def get_orders_query(self,db: Session, id_orders: int)->Orders:
        return db.query(Orders).filter(Orders.Id_Orders == id_orders).first()
    
    async def create_orders(self, db: Session, orders: Orders)->Orders:
        db_orders = Orders(**orders.dict())
        db.add(db_orders)
        db.commit()
        db.refresh(db_orders)
        return db_orders

    async def update_orders(self, db: Session, orders_id: int, db_orders_data: Orders)->Orders:
        db_orders = db.query(Orders).filter(Orders.Id_Orders == orders_id).first()
        if db_orders is None:
            return None
        for key, value in db_orders_data.__dict__.items():
            if hasattr(db_orders, key) and value is not None:
                setattr(db_orders, key, value)
        db.commit()
        return db_orders