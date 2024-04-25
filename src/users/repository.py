from sqlalchemy.orm import Session
from .models import Users

class UsersRepository:
    async def get_user(self,db: Session, user_id: int)->Users:
        return db.query(Users).filter(Users.Id_Users == user_id).first()

    async def get_all_users(self,db: Session)-> list[Users]:
        return db.query(Users).all()

    async def create_user(self,db: Session, user: Users)->Users:
        db_user = Users(**user.dict())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    async def update_user(self,db: Session, user_id: int, user_data: Users)->Users:
        db_user = db.query(Users).filter(Users.Id_Users == user_id).first()
        if db_user is None:
            return None
        for key, value in user_data.__dict__.items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
        return db_user