import datetime
from sqlalchemy.orm import Session
from .models import Users
from passlib.context import CryptContext
from common import generate_token
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UsersRepository:
    async def get_user(self,db: Session, user_id: int)->Users:
        return db.query(Users).filter(Users.Id_Users == user_id).first()
    
    async def get_user_mail(self,db: Session, mail: str)->Users:
        return db.query(Users).filter(Users.Mail == mail).first()


    async def get_all_users(self,db: Session)-> list[Users]:
        return db.query(Users).all()

    async def create_user(self,db: Session, user: Users)->Users:
        hashed_password = pwd_context.hash(user.Password)
        user.Password = hashed_password
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
    
    async def authenticate_user(self, db: Session, mail: str, password: str):
        user = await self.get_user_mail(db, mail)
        if user and pwd_context.verify(password, user.Password):
            token = generate_token(user.Id_Users)
            user.token = token
            user.token_creation_date = datetime.datetime.now(datetime.UTC)
            db.commit()
            db.refresh(user)
            return user
        return None