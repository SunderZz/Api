from sqlalchemy.orm import Session
from .models import Give_1

class Give_1Repository:

    async def create_give_1(self,db: Session, given: Give_1)->Give_1:
        db_given = Give_1(**given.dict())
        db.add(db_given)
        db.commit()
        db.refresh(db_given)
        return db_given

    async def get_give_1(self,db: Session)->Give_1:
        return db.query(Give_1).all()

    async def get_give_1_by_id(self,db: Session, id: int)->Give_1:
        return db.query(Give_1).filter(Give_1.Id_Notice == id).first()

    async def update_give_1(self,db: Session, id: int, given: Give_1)->Give_1:
        db_given = db.query(Give_1).filter(Give_1.Id_Notice == id).first()
        for key, value in given.dict().items():
            setattr(db_given, key, value)
        db.commit()
        db.refresh(db_given)
        return db_given
