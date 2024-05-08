from sqlalchemy.orm import Session
from .models import Customers

class CustomersRepository:
    async def get_customers(self, db: Session)->list[Customers]:
        return db.query(Customers).all()
    
    async def get_customers_query(self,db: Session, customers: int)->Customers:
        return db.query(Customers).filter(Customers.Id_Casual == customers).first()  


    async def create_customers(self, db: Session, customers: Customers)->Customers:
        db_customers = Customers(**customers.dict())
        db.add(db_customers)
        db.commit()
        db.refresh(db_customers)
        return db_customers

    async def update_customers(self, db: Session, customers: int, db_customers_data: Customers)->Customers:
        db_customers = db.query(Customers).filter(Customers.Id_Casual == customers).first()
        if db_customers is None:
            return None
        for key, value in db_customers_data.__dict__.items():
            if hasattr(db_customers, key) and value is not None:
                setattr(db_customers, key, value)
        db.commit()
        return db_customers