import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .models import Users
from .schema import UserCreate
from common import generate_token
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"])


class UsersRepository:
    def map_to_sqlalchemy(self, user_create: UserCreate) -> Users:
        return Users(
            F_Name=user_create.F_Name,
            Name=user_create.Name,
            Mail=user_create.Mail,
            Password=user_create.Password,
            active=user_create.active,
        )

    async def create_user(self, db: AsyncSession, user_create: UserCreate) -> Users:
        user = self.map_to_sqlalchemy(user_create)
        hashed_password = pwd_context.hash(user.Password)
        user.Password = hashed_password
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user

    async def get_user(self, db: AsyncSession, user_id: str) -> Users:
        result = await db.execute(select(Users).filter(Users.Id_Users == user_id))
        return result.scalar_one_or_none()
    
    async def delete_token(self, db: AsyncSession, user_id: str) -> None:
        result = await db.execute(select(Users).filter(Users.Id_Users == user_id))
        user = result.scalar_one_or_none()
        if user:
            user.token = None
            await db.commit()

    async def get_user_with_mail(self, db: AsyncSession, mail: str) -> Users:
        result = await db.execute(select(Users).filter(Users.Mail == mail))
        return result.scalar_one_or_none()

    async def get_user_with_token(self, db: AsyncSession, token: str) -> Users:
        result = await db.execute(select(Users).filter(Users.token == token))
        return result.scalar_one_or_none()

    async def get_all_users(self, db: AsyncSession) -> list[Users]:
        result = await db.execute(select(Users))
        return result.scalars().all()

    async def update_user(
        self, db: AsyncSession, user_id: int, user_data: UserCreate
    ) -> Users:
        result = await db.execute(select(Users).filter(Users.Id_Users == user_id))
        db_user = result.scalar_one_or_none()
        if db_user is None:
            return None

        for key, value in user_data.__dict__.items():
            if value is not None:
                if key == "Password":
                    hashed_password = pwd_context.hash(value)
                    setattr(db_user, key, hashed_password)
                else:
                    setattr(db_user, key, value)

        await db.commit()
        await db.refresh(db_user)
        return db_user

    async def authenticate_user(self, db: AsyncSession, mail: str, password: str):
        user = await self.get_user_with_mail(db, mail)
        if user and pwd_context.verify(password, user.Password):
            token = generate_token(user.Id_Users)
            user.token = token
            user.token_creation_date = datetime.datetime.utcnow()
            await db.commit()
            await db.refresh(user)
            return user
        return None
