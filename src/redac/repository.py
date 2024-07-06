from sqlalchemy.ext.asyncio import AsyncSession
from .models import Redact
from sqlalchemy.future import select


class RedactRepository:
    async def get_Redact(self, db: AsyncSession) -> list[Redact]:
        result = await db.execute(select(Redact))
        return result.scalars().all()

    async def get_Redact_by_admin_and_recipe(
        self, db: AsyncSession, admin_id: int, recipe_id: int
    ) -> Redact:
        result = await db.execute(
            select(Redact).filter(
                Redact.Id_Admin == admin_id, Redact.Id_Recipes == recipe_id
            )
        )
        return result.scalar_one_or_none()

    async def create_Redact(self, db: AsyncSession, redact: Redact) -> Redact:
        db_redact = Redact(**redact.dict())
        db.add(db_redact)
        await db.commit()
        await db.refresh(db_redact)
        return db_redact

    async def update_Redact(
        self, db: AsyncSession, admin_id: int, recipe_id: int, redact_data: Redact
    ) -> Redact:
        result = await db.execute(
            select(Redact).filter(
                Redact.Id_Admin == admin_id, Redact.Id_Recipes == recipe_id
            )
        )
        db_redact = result.scalar_one_or_none()
        if db_redact is None:
            return None
        for key, value in redact_data.dict().items():
            if hasattr(db_redact, key) and value is not None:
                setattr(db_redact, key, value)
        await db.commit()
        return db_redact
