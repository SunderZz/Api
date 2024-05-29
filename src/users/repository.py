import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .models import Users
from passlib.context import CryptContext
from common import generate_token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UsersRepository:
    async def get_user(self, db: AsyncSession, user_id: int) -> Users:
        result = await db.execute(select(Users).filter(Users.Id_Users == user_id))
        return result.scalar_one_or_none()
    
    async def get_user_mail(self, db: AsyncSession, mail: str) -> Users:
        result = await db.execute(select(Users).filter(Users.Mail == mail))
        return result.scalar_one_or_none()

    async def get_all_users(self, db: AsyncSession) -> list[Users]:
        result = await db.execute(select(Users))
        return result.scalars().all()

    async def create_user(self, db: AsyncSession, user: Users) -> Users:
        hashed_password = pwd_context.hash(user.Password)
        user.Password = hashed_password
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user

    async def update_user(self, db: AsyncSession, user_id: int, user_data: Users) -> Users:
        result = await db.execute(select(Users).filter(Users.Id_Users == user_id))
        db_user = result.scalar_one_or_none()
        if db_user is None:
            return None
        for key, value in user_data.__dict__.items():
            setattr(db_user, key, value)
        await db.commit()
        await db.refresh(db_user)
        return db_user
    
    async def authenticate_user(self, db: AsyncSession, mail: str, password: str):
        user = await self.get_user_mail(db, mail)
        if user and pwd_context.verify(password, user.Password):
            token = generate_token(user.Id_Users)
            user.token = token
            user.token_creation_date = datetime.datetime.utcnow()
            await db.commit()
            await db.refresh(user)
            return user
        return None
