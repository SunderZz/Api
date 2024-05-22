from sqlalchemy.orm import Session
from .models import Preferenceship   

class PreferenceshipRepository:

    async def create_preferenceship(self, db: Session, preferenceship: Preferenceship)->Preferenceship:
        db_preferenceship = Preferenceship(**preferenceship.dict())
        db.add(db_preferenceship)
        db.commit()
        db.refresh(db_preferenceship)
        return db_preferenceship

    async def update_preferenceship(self, db: Session, preferenceship: int, db_preferenceship_data: Preferenceship)->Preferenceship:
        db_preferenceship = db.query(Preferenceship).filter(Preferenceship.Id_Preferenceship == preferenceship).first()
        if db_preferenceship is None:
            return None
        for key, value in db_preferenceship_data.__dict__.items():
            if hasattr(db_preferenceship, key) and value is not None:
                setattr(db_preferenceship, key, value)
        db.commit()
        return db_preferenceship
    
    async def create_preference_ship(self,db: Session, preferenceship: Preferenceship) -> Preferenceship:
        preferenceship_data = preferenceship.dict(by_alias=True)
        db_address = Preferenceship(**preferenceship_data)
        db.add(db_address)
        db.commit()
        db.refresh(db_address)
        return db_address