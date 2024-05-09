from sqlalchemy.orm import Session
from.models import Redact

class RedactRepository:
    async def get_Redact(self, db: Session) -> Redact:
        return db.query(Redact).all()
    
    async def get_Redact_by_admin_and_recipe(self, db: Session, admin_id: int, recipe_id: int) -> Redact:
        return db.query(Redact).filter(Redact.Id_Admin == admin_id, Redact.Id_Recipes == recipe_id).first()
    
    async def create_Redact(self, db: Session, redact: Redact) -> Redact:
        db_redact = Redact(**redact.dict())
        db.add(db_redact)
        db.commit()
        db.refresh(db_redact)
        return db_redact

    async def update_Redact(self, db: Session, admin_id: int, recipe_id: int, redact_data: Redact) -> Redact:
        db_redact = db.query(Redact).filter(Redact.Id_Admin == admin_id, Redact.Id_Recipes == recipe_id).first()
        if db_redact is None:
            return None
        for key, value in redact_data.__dict__.items():
            if hasattr(db_redact, key) and value is not None:
                setattr(db_redact, key, value)
        db.commit()
        return db_redact