from sqlalchemy.orm import Session
from .models import Payment

class PaymentRepository:
    async def get_payment(self, db: Session)->list[Payment]:
        return db.query(Payment).all()
    
    async def get_payment_query(self,db: Session, payment: int)->Payment:
        return db.query(Payment).filter(Payment.Id_Payments == payment).first()
    
    async def create_payment(self, db: Session, payment: Payment)->Payment:
        db_payment = Payment(**payment.dict())
        db.add(db_payment)
        db.commit()
        db.refresh(db_payment)
        return db_payment

    async def update_payment(self, db: Session, payment_id: int, db_payment_data: Payment)->Payment:
        db_payment = db.query(Payment).filter(Payment.Id_Payments == payment_id).first()
        if db_payment is None:
            return None
        for key, value in db_payment_data.__dict__.items():
            if hasattr(db_payment, key) and value is not None:
                setattr(db_payment, key, value)
        db.commit()
        return db_payment