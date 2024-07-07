from sqlalchemy.ext.asyncio import AsyncSession
from .models import Preferenceship


class PreferenceshipRepository:

    async def create_preferenceship(
        self, db: AsyncSession, preferenceship: Preferenceship
    ) -> Preferenceship:
        db_preferenceship = Preferenceship(**preferenceship.dict())
        db.add(db_preferenceship)
        await db.commit()
        await db.refresh(db_preferenceship)
        return db_preferenceship
