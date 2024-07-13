from sqlalchemy.ext.asyncio import AsyncSession
from .models import Adresse_Type
from sqlalchemy.future import select


class AdresseTypesRepository:
    async def get_adressestypes(self, db: AsyncSession) -> list[Adresse_Type]:
        result = await db.execute(select(Adresse_Type))
        return result.scalars().all()

    async def get_adressestypes_query(
        self, db: AsyncSession, adressestypes: int
    ) -> Adresse_Type:
        result = await db.execute(
            select(Adresse_Type).filter(Adresse_Type.Id_Adresse_Type == adressestypes)
        )
        return result.scalar_one_or_none()

    async def get_adressestypes_user(
        self, db: AsyncSession, id_user: int
    ) -> Adresse_Type:
        result = await db.execute(
            select(Adresse_Type).filter(Adresse_Type.Id_Users == id_user)
        )
        return result.scalar_one_or_none()

    async def create_adressestypes(
        self, db: AsyncSession, adressestypes: Adresse_Type
    ) -> Adresse_Type:
        db_adressestypes = Adresse_Type(**adressestypes.dict())
        db.add(db_adressestypes)
        await db.commit()
        await db.refresh(db_adressestypes)
        return db_adressestypes

    async def update_adressestypes(
        self, db: AsyncSession, adressestypes: int, db_adressestypes_data: Adresse_Type
    ) -> Adresse_Type:
        result = await db.execute(
            select(Adresse_Type).filter(Adresse_Type.Id_Adresse_Type == adressestypes)
        )
        db_adressestypes = result.scalar_one_or_none()
        if db_adressestypes is None:
            return None
        for key, value in db_adressestypes_data.__dict__.items():
            if hasattr(db_adressestypes, key) and value is not None:
                setattr(db_adressestypes, key, value)
        await db.commit()
        return db_adressestypes
