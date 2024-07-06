from sqlalchemy.ext.asyncio import AsyncSession
from .models import Notice
from sqlalchemy.future import select


class NoticeRepository:
    async def get_notice(self, db: AsyncSession) -> list[Notice]:
        result = await db.execute(select(Notice))
        return result.scalars().all()

    async def create_notice(self, db: AsyncSession, notice: Notice) -> Notice:
        db_notice = Notice(**notice.dict())
        db.add(db_notice)
        await db.commit()
        await db.refresh(db_notice)
        return db_notice

    async def get_notice_by_id(
        self, db: AsyncSession, notice: int
    ) -> list[Notice] | Notice | None:
        result = await db.execute(select(Notice).filter(Notice.Id_Notice == notice))
        return result.scalars().all()
