from sqlalchemy.orm import Session
from.models import Operate

class OperateRepository:

    async def create_operate(self,db: Session, operate: Operate)->Operate:
        db_operate = Operate(**operate.dict())
        db.add(db_operate)
        db.commit()
        db.refresh(db_operate)
        return db_operate

    async def get_operate(self,db: Session)->Operate:
        return db.query(Operate).all()

    async def get_operate_by_id(self,db: Session, id: int)->Operate:
        return db.query(Operate).filter(Operate.Id_Casual == id).first()

    async def update_operate(self,db: Session, id: int, operate: Operate)->Operate:
        db_operate = db.query(Operate).filter(Operate.Id_Casual == id).first()
        for key, value in operate.dict().items():
            setattr(db_operate, key, value)
        db.commit()
        db.refresh(db_operate)
        return db_operate
