from sqlalchemy.ext.asyncio import AsyncSession
from .models import Asso_33
from sqlalchemy.future import select

class Asso_33Repository:

    async def create_asso_33(self, db: AsyncSession, asso: Asso_33) -> Asso_33:
        db_given = Asso_33(**asso.dict())
        db.add(db_given)
        await db.commit()
        await db.refresh(db_given)
        return db_given

    async def get_asso_33(self, db: AsyncSession) -> list[Asso_33]:
        result = await db.execute(select(Asso_33))
        return result.scalars().all()

    async def get_asso_33_by_id(self, db: AsyncSession, id: int) -> Asso_33:
        result = await db.execute(select(Asso_33).filter(Asso_33.Id_Users_adresses == id))
        return result.scalar_one_or_none()

    async def update_asso_33(self, db: AsyncSession, id: int, asso: Asso_33) -> Asso_33:
        result = await db.execute(select(Asso_33).filter(Asso_33.Id_Users_adresses == id))
        db_given = result.scalar_one_or_none()
        if db_given:
            for key, value in asso.dict().items():
                setattr(db_given, key, value)
            await db.commit()
            await db.refresh(db_given)
        return db_given
