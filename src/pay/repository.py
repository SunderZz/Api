from sqlalchemy.orm import Session
from.models import Pay

class PayRepository:

    async def create_pay(self,db: Session, pay: Pay)->Pay:
        db_pay = Pay(**pay.dict())
        db.add(db_pay)
        db.commit()
        db.refresh(db_pay)
        return db_pay

    async def get_pays(self,db: Session)->Pay:
        return db.query(Pay).all()

    async def get_pay_by_id(self,db: Session, id: int)->Pay:
        return db.query(Pay).filter(Pay.Id_Payments == id).first()

    async def update_pay(self,db: Session, id: int, pay: Pay)->Pay:
        db_pay = db.query(Pay).filter(Pay.Id_Payments == id).first()
        for key, value in pay.dict().items():
            setattr(db_pay, key, value)
        db.commit()
        db.refresh(db_pay)
        return db_pay
