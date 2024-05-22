from sqlalchemy.orm import Session
from .models import Linede

class LinedeRepository:

    async def create_linede(self,db: Session, linede: Linede )->Linede:
        db_linede = Linede(**linede.dict())
        db.add(db_linede)
        db.commit()
        db.refresh(db_linede)
        return db_linede

    async def get_linede(self,db: Session)->Linede:
        return db.query(Linede).all()

    async def get_linede_by_id(self, db: Session, id: int) -> Linede | list[Linede]:
            result = db.query(Linede).filter(Linede.Id_Orders == id).all()
            
            if not result:
                return []  
            
            if len(result) > 1:
                return result
            
            return result[0]

    async def update_linede(self,db: Session, id: int, linede: Linede)->Linede:
        db_linede = db.query(Linede).filter(Linede.Id_Orders == id).first()
        for key, value in linede.dict().items():
            setattr(db_linede, key, value)
        db.commit()
        db.refresh(db_linede)
        return db_linede


    async def add_products_to_order(self, db: Session, linede: Linede|list[Linede] ) -> list[Linede] | Linede:
        if isinstance(linede, list):
            for line in linede:
                lignes = []
                db_linede = Linede(**line.dict())
                db.add(db_linede)
                db.commit()
                db.refresh(db_linede)
                lignes.append(db_linede)
            return lignes
        else:
            db_linede = Linede(**linede.dict())
            db.add(db_linede)
            db.commit()
            db.refresh(db_linede)
            return db_linede
        