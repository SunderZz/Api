from sqlalchemy.orm import Session
from.models import Manage

class ManageRepository:

    async def create_manage(self,db: Session, manage: Manage)->Manage:
        db_manage = Manage(**manage.dict())
        db.add(db_manage)
        db.commit()
        db.refresh(db_manage)
        return db_manage

    async def get_manage(self,db: Session)->Manage:
        return db.query(Manage).all()

    async def get_manage_by_id(self,db: Session, id: int)->Manage:
        return db.query(Manage).filter(Manage.Id_Product == id).first()

    async def update_manage(self,db: Session, id: int, manage: Manage)->Manage:
        db_manage = db.query(Manage).filter(Manage.Id_Product == id).first()
        for key, value in manage.dict().items():
            setattr(db_manage, key, value)
        db.commit()
        db.refresh(db_manage)
        return db_manage
