from sqlalchemy.orm import Session
from .models import Give

class GiveRepository:

    async def create_give(self,db: Session, give: Give)->Give:
        db_given = Give(**give.dict())
        db.add(db_given)
        db.commit()
        db.refresh(db_given)
        return db_given

    async def get_give(self,db: Session)->Give:
        return db.query(Give).all()

    async def get_give_by_id(self,db: Session, id: int)->Give:
        return db.query(Give).filter(Give.Id_Product == id).first()

    async def update_give(self,db: Session, id: int, give: Give)->Give:
        db_given = db.query(Give).filter(Give.Id_Product == id).first()
        for key, value in give.dict().items():
            setattr(db_given, key, value)
        db.commit()
        db.refresh(db_given)
        return db_given
