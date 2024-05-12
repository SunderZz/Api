from sqlalchemy.orm import Session
from .models import Is_On

class IsOnRepository:

    async def create_is_on(self,db: Session, is_On: Is_On)->Is_On:
        db_is_On = Is_On(**is_On.dict())
        db.add(db_is_On)
        db.commit()
        db.refresh(db_is_On)
        return db_is_On

    async def get_is_on(self,db: Session)->Is_On:
        return db.query(Is_On).all()

    async def get_is_on_by_id(self,db: Session, id: int)->Is_On:
        return db.query(Is_On).filter(Is_On.Id_Product == id).first()

    async def update_is_on(self,db: Session, id: int, is_On: Is_On)->Is_On:
        db_is_On = db.query(Is_On).filter(Is_On.Id_Product == id).first()
        for key, value in is_On.dict().items():
            setattr(db_is_On, key, value)
        db.commit()
        db.refresh(db_is_On)
        return db_is_On
