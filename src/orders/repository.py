from sqlalchemy.ext.asyncio import AsyncSession
from .models import Orders
from sqlalchemy.future import select


class OrdersRepository:
    async def get_orders(self, db: AsyncSession) -> list[Orders]:
        result = await db.execute(select(Orders))
        return result.scalars().all()

    async def get_orders_query(self, db: AsyncSession, id_orders: int) -> Orders:
        result = await db.execute(select(Orders).filter(Orders.Id_Orders == id_orders))
        return result.scalar_one_or_none()
    
    async def get_all_order_of_customer(self, db: AsyncSession, id_casual: int) -> Orders:
        result = await db.execute(select(Orders).filter(Orders.Id_Casual == id_casual))
        return result.scalars().all()

    async def create_orders(self, db: AsyncSession, orders: Orders) -> Orders:
        db_orders = Orders(**orders.dict())
        db.add(db_orders)
        await db.commit()
        await db.refresh(db_orders)
        return db_orders

    async def update_orders(
        self, db: AsyncSession, orders_id: int, db_orders_data: Orders
    ) -> Orders:
        result = await db.execute(select(Orders).filter(Orders.Id_Orders == orders_id))
        db_orders = result.scalar_one_or_none()
        if db_orders is None:
            return None
        for key, value in db_orders_data.__dict__.items():
            if hasattr(db_orders, key) and value is not None:
                setattr(db_orders, key, value)
        await db.commit()
        return db_orders
