from sqlalchemy.orm import Session
from .models import Adresse_Type

class AdresseTypesRepository:
    async def get_adressestypes(self, db: Session)->list[Adresse_Type]:
        return db.query(Adresse_Type).all()
    
    async def get_adressestypes_query(self,db: Session, adressestypes: int)->Adresse_Type:
        return db.query(Adresse_Type).filter(Adresse_Type.Id_Adresse_Type == adressestypes).first()  


    async def create_adressestypes(self, db: Session, adressestypes: Adresse_Type)->Adresse_Type:
        db_adressestypes = Adresse_Type(**adressestypes.dict())
        db.add(db_adressestypes)
        db.commit()
        db.refresh(db_adressestypes)
        return db_adressestypes

    async def update_adressestypes(self, db: Session, adressestypes: int, db_adressestypes_data: Adresse_Type)->Adresse_Type:
        db_adressestypes = db.query(Adresse_Type).filter(Adresse_Type.Id_Adresse_Type == adressestypes).first()
        if db_adressestypes is None:
            return None
        for key, value in db_adressestypes_data.__dict__.items():
            if hasattr(db_adressestypes, key) and value is not None:
                setattr(db_adressestypes, key, value)
        db.commit()
        return db_adressestypes