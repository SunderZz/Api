from sqlalchemy.orm import Session
from.models import Located

class LocatedRepository:

    async def create_located(self,db: Session, located: Located)->Located:
        db_located = Located(**located.dict())
        db.add(db_located)
        db.commit()
        db.refresh(db_located)
        return db_located

    async def get_located(self,db: Session)->Located:
        return db.query(Located).all()

    async def get_located_by_id(self,db: Session, id: int)->Located:
        return db.query(Located).filter(Located.Id_Users_adresses == id).first()

    async def update_located(self,db: Session, id: int, located: Located)->Located:
        db_located = db.query(Located).filter(Located.Id_Users_adresses == id).first()
        for key, value in located.dict().items():
            setattr(db_located, key, value)
        db.commit()
        db.refresh(db_located)
        return db_located
