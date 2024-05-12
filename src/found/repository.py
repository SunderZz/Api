from sqlalchemy.orm import Session
from .models import Found

class FoundRepository:

    async def create_found(self,db: Session, found: Found)->Found:
        db_given = Found(**found.dict())
        db.add(db_given)
        db.commit()
        db.refresh(db_given)
        return db_given

    async def get_found(self,db: Session)->Found:
        return db.query(Found).all()

    async def get_found_by_id(self,db: Session, id: int)->Found:
        return db.query(Found).filter(Found.Id_Product == id).first()

    async def update_found(self,db: Session, id: int, found: Found)->Found:
        db_given = db.query(Found).filter(Found.Id_Product == id).first()
        for key, value in found.dict().items():
            setattr(db_given, key, value)
        db.commit()
        db.refresh(db_given)
        return db_given
