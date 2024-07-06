from sqlalchemy.ext.asyncio import AsyncSession
from .models import Tva
from sqlalchemy.future import select


class TvaRepository:
    async def get_tva(self, db: AsyncSession, tva_id: int):
        result = await db.execute(select(Tva).filter(Tva.Id_Tva == tva_id))
        return result.scalar_one_or_none()

    async def get_all_tva(self, db: AsyncSession) -> list[Tva]:
        result = await db.execute(select(Tva))
        return result.scalars().all()

    async def get_tva_by_name(self, db: AsyncSession, name: str):
        result = await db.execute(select(Tva).filter(Tva.Name == name))
        return result.scalar_one_or_none()

    async def create_tva(self, db: AsyncSession, tva: Tva):
        db_tva = Tva(**tva.dict())
        db.add(db_tva)
        await db.commit()
        await db.refresh(db_tva)
        return db_tva

    async def update_tva(self, db: AsyncSession, tva: Tva, tva_id: int):
        result = await db.execute(select(Tva).filter(Tva.Id_Tva == tva_id))
        db_tva = result.scalar_one_or_none()
        if db_tva is None:
            return None
        for key, value in tva.dict().items():
            setattr(db_tva, key, value)
        await db.commit()
        return db_tva

    async def calculate_tva(self, db: AsyncSession, price: float, tva_name: str):
        tva = await self.get_tva_by_name(db, tva_name)
        if tva is None:
            return None
        return price * (tva.Rate / 100)
