from sqlalchemy.ext.asyncio import AsyncSession
from .models import Manage
from sqlalchemy.future import select


class ManageRepository:

    async def create_manage(self, db: AsyncSession, manage: Manage) -> Manage:
        db_manage = Manage(**manage.dict())
        db.add(db_manage)
        await db.commit()
        await db.refresh(db_manage)
        return db_manage

    async def get_manage(self, db: AsyncSession) -> list[Manage]:
        result = await db.execute(select(Manage))
        return result.scalars().all()

    async def get_manage_by_id(self, db: AsyncSession, id: int) -> Manage:
        result = await db.execute(select(Manage).filter(Manage.Id_Product == id))
        return result.scalar_one_or_none()

    async def update_manage(self, db: AsyncSession, id: int, manage: Manage) -> Manage:
        result = await db.execute(select(Manage).filter(Manage.Id_Product == id))
        db_manage = result.scalar_one_or_none()
        if db_manage:
            for key, value in manage.dict().items():
                setattr(db_manage, key, value)
            await db.commit()
            await db.refresh(db_manage)
        return db_manage
