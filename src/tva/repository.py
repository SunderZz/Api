from sqlalchemy.orm import Session
from .models import Tva

class TvaRepository:
    async def get_tva(self, db: Session, tva_id: int):
        return db.query(Tva).filter(Tva.Id_Tva == tva_id).first()
    
    async def get_all_tva(self, db: Session)->list[Tva]:
        return db.query(Tva).all()

    async def get_tva_by_name(self, db: Session, name: str):
        return db.query(Tva).filter(Tva.Name == name).first()

    async def create_tva(self, db: Session, tva: Tva):
        db_tva = Tva(**tva.dict())
        db.add(db_tva)
        db.commit()
        db.refresh(db_tva)
        return db_tva

    async def update_tva(self, db: Session, tva: Tva, tva_id: int):
        db_tva = db.query(Tva).filter(Tva.Id_Tva == tva_id).first()
        if db_tva is None:
            return None
        for key, value in tva.dict().items():
            setattr(db_tva, key, value)
        db.commit()
        return db_tva

    async def calculate_tva(self, db: Session, price: float, tva_name: str):
        tva = await self.get_tva_by_name(db, tva_name)
        if tva is None:
            return None
        return price * (tva.Rate / 100)