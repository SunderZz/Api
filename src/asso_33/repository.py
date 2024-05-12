from sqlalchemy.orm import Session
from .models import Asso_33

class Asso_33Repository:

    async def create_asso_33(self,db: Session, asso: Asso_33)->Asso_33:
        db_given = Asso_33(**asso.dict())
        db.add(db_given)
        db.commit()
        db.refresh(db_given)
        return db_given

    async def get_asso_33(self,db: Session)->Asso_33:
        return db.query(Asso_33).all()

    async def get_asso_33_by_id(self,db: Session, id: int)->Asso_33:
        return db.query(Asso_33).filter(Asso_33.Id_Users_adresses == id).first()

    async def update_asso_33(self,db: Session, id: int, asso: Asso_33)->Asso_33:
        db_given = db.query(Asso_33).filter(Asso_33.Id_Users_adresses == id).first()
        for key, value in asso.dict().items():
            setattr(db_given, key, value)
        db.commit()
        db.refresh(db_given)
        return db_given
