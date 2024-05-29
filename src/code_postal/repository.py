from sqlalchemy.ext.asyncio import AsyncSession
from .models import Code_Postal
from sqlalchemy.future import select

class CodePostalRepository:
    async def get_code_postal(self, db: AsyncSession) -> list[Code_Postal]:
        result = await db.execute(select(Code_Postal))
        return result.scalars().all()
    
    async def get_code_postal_query(self, db: AsyncSession, code_postal: int) -> Code_Postal:
        result = await db.execute(select(Code_Postal).filter(Code_Postal.code_postal == code_postal))
        return result.scalar_one_or_none()

    async def create_code_postal(self, db: AsyncSession, code_postal: Code_Postal) -> Code_Postal:
        db_code_postal = Code_Postal(**code_postal.dict())
        db.add(db_code_postal)
        await db.commit()
        await db.refresh(db_code_postal)
        return db_code_postal

    async def update_code_postal(self, db: AsyncSession, code_postal: int, db_code_postal_data: Code_Postal) -> Code_Postal:
        result = await db.execute(select(Code_Postal).filter(Code_Postal.Id_Code_Postal == code_postal))
        db_code_postal = result.scalar_one_or_none()
        if db_code_postal:
            for key, value in db_code_postal_data.__dict__.items():
                if hasattr(db_code_postal, key) and value is not None:
                    setattr(db_code_postal, key, value)
            await db.commit()
        return db_code_postal
