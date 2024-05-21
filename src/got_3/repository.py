from sqlalchemy.orm import Session
from .models import Got

class GotRepository:

    async def create_got(self,db: Session, got: Got)->Got:
        db_Got = Got(**got.dict())
        db.add(db_Got)
        db.commit()
        db.refresh(db_Got)
        return db_Got

    async def get_got(self,db: Session)->Got:
        return db.query(Got).all()

    async def get_got_by_id(self,db: Session, id: int)->Got:
        return db.query(Got).filter(Got.Id_City == id).first()

    async def update_got(self,db: Session, got: Got, id: int|None = None)->Got:
        db_Got = db.query(Got).filter(Got.Id_City == id).first()
        for key, value in got.dict().items():
            setattr(db_Got, key, value)
        db.commit()
        db.refresh(db_Got)
        return db_Got
