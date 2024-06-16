from sqlalchemy.ext.asyncio import AsyncSession
from .models import Customers
from sqlalchemy.future import select

class CustomersRepository:
    async def get_customers(self, db: AsyncSession) -> list[Customers]:
        result = await db.execute(select(Customers))
        return result.scalars().all()
    
    async def get_customers_query(self, db: AsyncSession, customers: int) -> Customers:
        result = await db.execute(select(Customers).filter(Customers.Id_Users == customers))
        return result.scalar_one_or_none()

    async def create_customers(self, db: AsyncSession, customers: Customers) -> Customers:
        db_customers = Customers(**customers.dict())
        db.add(db_customers)
        await db.commit()
        await db.refresh(db_customers)
        return db_customers

    async def update_customers(self, db: AsyncSession, customers: int, db_customers_data: Customers) -> Customers:
        result = await db.execute(select(Customers).filter(Customers.Id_Casual == customers))
        db_customers = result.scalar_one_or_none()
        if db_customers:
            for key, value in db_customers_data.__dict__.items():
                if hasattr(db_customers, key) and value is not None:
                    setattr(db_customers, key, value)
            await db.commit()
        return db_customers
