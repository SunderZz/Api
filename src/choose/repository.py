from sqlalchemy.orm import Session
from .models import Choose

class ChooseRepository:

    async def create_choose(self,db: Session, choose: Choose)->Choose:
        db_given = Choose(**choose.dict())
        db.add(db_given)
        db.commit()
        db.refresh(db_given)
        return db_given

    async def get_choose(self,db: Session)->Choose:
        return db.query(Choose).all()

    async def get_choose_by_id(self,db: Session, id: int)->Choose:
        return db.query(Choose).filter(Choose.Id_Product == id).first()

    async def update_choose(self,db: Session, id: int, choose: Choose)->Choose:
        db_given = db.query(Choose).filter(Choose.Id_Product == id).first()
        for key, value in choose.dict().items():
            setattr(db_given, key, value)
        db.commit()
        db.refresh(db_given)
        return db_given
