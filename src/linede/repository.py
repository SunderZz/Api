from sqlalchemy.ext.asyncio import AsyncSession
from .models import Linede
from sqlalchemy.future import select

class LinedeRepository:

    async def create_linede(self, db: AsyncSession, linede: Linede) -> Linede:
        db_linede = Linede(**linede.dict())
        db.add(db_linede)
        await db.commit()
        await db.refresh(db_linede)
        return db_linede

    async def get_linede(self, db: AsyncSession) -> list[Linede]:
        result = await db.execute(select(Linede))
        return result.scalars().all()

    async def get_linede_by_id(self, db: AsyncSession, id: int) -> Linede | list[Linede]:
        result = await db.execute(select(Linede).filter(Linede.Id_Orders == id))
        linedes = result.scalars().all()
        
        if not linedes:
            return []

        if len(linedes) > 1:
            return linedes
        
        return linedes[0]

    async def update_linede(self, db: AsyncSession, id: int, linede: Linede) -> Linede:
        result = await db.execute(select(Linede).filter(Linede.Id_Orders == id))
        db_linede = result.scalar_one_or_none()
        if db_linede:
            for key, value in linede.dict().items():
                setattr(db_linede, key, value)
            await db.commit()
            await db.refresh(db_linede)
        return db_linede

    async def add_products_to_order(self, db: AsyncSession, linede: Linede | list[Linede]) -> list[Linede] | Linede:
        if isinstance(linede, list):
            lignes = []
            for line in linede:
                db_linede = Linede(**line.dict())
                db.add(db_linede)
                await db.commit()
                await db.refresh(db_linede)
                lignes.append(db_linede)
            return lignes
        else:
            db_linede = Linede(**linede.dict())
            db.add(db_linede)
            await db.commit()
            await db.refresh(db_linede)
            return db_linede
