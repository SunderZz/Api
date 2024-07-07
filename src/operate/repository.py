from sqlalchemy.ext.asyncio import AsyncSession
from .models import Operate
from sqlalchemy.future import select


class OperateRepository:

    async def create_operate(self, db: AsyncSession, operate: Operate) -> Operate:
        db_operate = Operate(**operate.dict())
        db.add(db_operate)
        await db.commit()
        await db.refresh(db_operate)
        return db_operate

    async def get_operate(self, db: AsyncSession) -> list[Operate]:
        result = await db.execute(select(Operate))
        return result.scalars().all()

    async def get_operate_by_id(self, db: AsyncSession, id: int) -> Operate:
        result = await db.execute(select(Operate).filter(Operate.Id_Casual == id))
        return result.scalar_one_or_none()
