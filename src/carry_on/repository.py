from sqlalchemy.orm import Session
from .models import CarryOn

class CarryOnRepository:

    async def create_carry_on(self,db: Session, carry_on: CarryOn)->CarryOn:
        db_given = CarryOn(**carry_on.dict())
        db.add(db_given)
        db.commit()
        db.refresh(db_given)
        return db_given

    async def get_carry_on(self,db: Session)->CarryOn:
        return db.query(CarryOn).all()

    async def get_carry_on_by_id(self,db: Session, id: int)->CarryOn:
        return db.query(CarryOn).filter(CarryOn.Id_Producers == id).first()

    async def update_carry_on(self,db: Session, id: int, carry_on: CarryOn)->CarryOn:
        db_given = db.query(CarryOn).filter(CarryOn.Id_Producers == id).first()
        for key, value in carry_on.dict().items():
            setattr(db_given, key, value)
        db.commit()
        db.refresh(db_given)
        return db_given
