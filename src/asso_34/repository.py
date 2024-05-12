from sqlalchemy.orm import Session
from .models import Asso_34

class Asso_34Repository:

    async def create_asso_34(self,db: Session, asso: Asso_34)->Asso_34:
        db_given = Asso_34(**asso.dict())
        db.add(db_given)
        db.commit()
        db.refresh(db_given)
        return db_given

    async def get_asso_34(self,db: Session)->Asso_34:
        return db.query(Asso_34).all()

    async def get_asso_34_by_id(self,db: Session, id: int)->Asso_34:
        return db.query(Asso_34).filter(Asso_34.Id_Orders == id).first()

    async def update_asso_34(self,db: Session, id: int, asso: Asso_34)->Asso_34:
        db_given = db.query(Asso_34).filter(Asso_34.Id_Orders == id).first()
        for key, value in asso.dict().items():
            setattr(db_given, key, value)
        db.commit()
        db.refresh(db_given)
        return db_given
