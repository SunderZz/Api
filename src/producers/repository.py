from sqlalchemy.orm import Session
from .models import Producers

class ProducersRepository:
    async def get_producers(self, db: Session)->list[Producers]:
        return db.query(Producers).all()
    
    async def get_producers_query(self,db: Session, producers: int)->Producers:
        return db.query(Producers).filter(Producers.Id_Producers == producers).first()  


    async def create_producers(self, db: Session, producers: Producers)->Producers:
        db_producers = Producers(**producers.dict())
        db.add(db_producers)
        db.commit()
        db.refresh(db_producers)
        return db_producers

    async def update_producers(self, db: Session, producers: int, db_producers_data: Producers)->Producers:
        db_producers = db.query(Producers).filter(Producers.Id_Producers == producers).first()
        if db_producers is None:
            return None
        for key, value in db_producers_data.__dict__.items():
            if hasattr(db_producers, key) and value is not None:
                setattr(db_producers, key, value)
        db.commit()
        return db_producers