from sqlalchemy.orm import Session
from .models import Unit

class UnitRepository:
    async def get_units(self, db: Session)->Unit:
        return db.query(Unit).first()
    
    
    async def create_unit(self, db: Session, unit: Unit)->Unit:
        db_unit = Unit(**unit.dict())
        db.add(db_unit)
        db.commit()
        db.refresh(db_unit)
        return db_unit

    async def update_unit(self, db: Session, unit_id: int, unit_data: Unit)->Unit:
        db_unit = db.query(Unit).filter(Unit.Id_Unit == unit_id).first()
        if db_unit is None:
            return None
        for key, value in unit_data.__dict__.items():
            if hasattr(db_unit, key) and value is not None:
                setattr(db_unit, key, value)
        db.commit()
        return db_unit