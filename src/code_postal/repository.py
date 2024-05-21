from sqlalchemy.orm import Session
from .models import Code_Postal

class CodePostalRepository:
    async def get_code_postal(self, db: Session)->list[Code_Postal]:
        return db.query(Code_Postal).all()
    
    async def get_code_postal_query(self,db: Session, code_postal: int)->Code_Postal:
        return db.query(Code_Postal).filter(Code_Postal.code_postal == code_postal).first()  


    async def create_code_postal(self, db: Session, code_postal: Code_Postal)->Code_Postal:
        db_code_postal = Code_Postal(**code_postal.dict())
        db.add(db_code_postal)
        db.commit()
        db.refresh(db_code_postal)
        return db_code_postal

    async def update_code_postal(self, db: Session, code_postal: int, db_code_postal_data: Code_Postal)->Code_Postal:
        db_code_postal = db.query(Code_Postal).filter(Code_Postal.Id_Code_Postal == code_postal).first()
        if db_code_postal is None:
            return None
        for key, value in db_code_postal_data.__dict__.items():
            if hasattr(db_code_postal, key) and value is not None:
                setattr(db_code_postal, key, value)
        db.commit()
        return db_code_postal