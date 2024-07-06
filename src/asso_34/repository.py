from sqlalchemy.ext.asyncio import AsyncSession
from .models import Asso_34
from sqlalchemy.future import select


class Asso_34Repository:

    async def create_asso_34(self, db: AsyncSession, asso: Asso_34) -> Asso_34:
        db_given = Asso_34(**asso.dict())
        db.add(db_given)
        await db.commit()
        await db.refresh(db_given)
        return db_given

    async def get_asso_34(self, db: AsyncSession) -> list[Asso_34]:
        result = await db.execute(select(Asso_34))
        return result.scalars().all()

    async def get_asso_34_by_id(self, db: AsyncSession, id: int) -> Asso_34:
        result = await db.execute(select(Asso_34).filter(Asso_34.Id_Orders == id))
        return result.scalar_one_or_none()

    async def update_asso_34(self, db: AsyncSession, id: int, asso: Asso_34) -> Asso_34:
        result = await db.execute(select(Asso_34).filter(Asso_34.Id_Orders == id))
        db_given = result.scalar_one_or_none()
        if db_given:
            for key, value in asso.dict().items():
                setattr(db_given, key, value)
            await db.commit()
            await db.refresh(db_given)
        return db_given
