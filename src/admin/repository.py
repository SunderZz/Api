from sqlalchemy.orm import Session
from .models import Admin

class AdminRepository:
    async def get_admin(self, db: Session)->list[Admin]:
        return db.query(Admin).all()
    
    async def get_admin_query(self,db: Session, admin: int)->Admin:
        return db.query(Admin).filter(Admin.Id_Admin == admin).first()  


    async def create_admin(self, db: Session, admin: Admin)->Admin:
        db_admin = Admin(**admin.dict())
        db.add(db_admin)
        db.commit()
        db.refresh(db_admin)
        return db_admin

    async def update_admin(self, db: Session, admin: int, db_admin_data: Admin)->Admin:
        db_admin = db.query(Admin).filter(Admin.Id_Admin == admin).first()
        if db_admin is None:
            return None
        for key, value in db_admin_data.__dict__.items():
            if hasattr(db_admin, key) and value is not None:
                setattr(db_admin, key, value)
        db.commit()
        return db_admin