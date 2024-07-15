from sqlalchemy.ext.asyncio import AsyncSession
from .models import Given
from sqlalchemy.future import select


class GivenRepository:

    async def create_given(self, db: AsyncSession, given: Given) -> Given:
        db_given = Given(**given.dict())
        db.add(db_given)
        await db.commit()
        await db.refresh(db_given)
        return db_given

    async def get_given(self, db: AsyncSession) -> list[Given]:
        result = await db.execute(select(Given))
        return result.scalars().all()

    async def get_given_by_id(self, db: AsyncSession, id: int) -> Given:
        result = await db.execute(select(Given).filter(Given.Id_Notice == id))
        return result.scalar_one_or_none()

    async def get_notice_by_product(
        self, db: AsyncSession, product: int
    ) -> list[Given] | None:
        result = await db.execute(select(Given).filter(Given.Id_Product == product))
        return result.scalars().all()

    async def update_given(self, db: AsyncSession, id: int, given: Given) -> Given:
        result = await db.execute(select(Given).filter(Given.Id_Notice == id))
        db_given = result.scalar_one_or_none()
        if db_given:
            for key, value in given.dict().items():
                setattr(db_given, key, value)
            await db.commit()
            await db.refresh(db_given)
        return db_given
