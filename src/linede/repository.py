from sqlalchemy.orm import Session
from .models import Linede

class LinedeRepository:

    async def create_linede(self,db: Session, linede: Linede)->Linede:
        db_linede = Linede(**linede.dict())
        db.add(db_linede)
        db.commit()
        db.refresh(db_linede)
        return db_linede

    async def get_linede(self,db: Session)->Linede:
        return db.query(Linede).all()

    async def get_linede_by_id(self,db: Session, id: int)->Linede:
        return db.query(Linede).filter(Linede.Id_Orders == id).first()

    async def update_linede(self,db: Session, id: int, linede: Linede)->Linede:
        db_linede = db.query(Linede).filter(Linede.Id_Orders == id).first()
        for key, value in linede.dict().items():
            setattr(db_linede, key, value)
        db.commit()
        db.refresh(db_linede)
        return db_linede
