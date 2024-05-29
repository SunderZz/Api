from sqlalchemy.ext.asyncio import AsyncSession
from .models import Shipments_Cost
from sqlalchemy.future import select

class ShipmentsCostRepository:
    async def get_shipments_Costs(self, db: AsyncSession) -> list[Shipments_Cost]:
        result = await db.execute(select(Shipments_Cost))
        return result.scalars().all()
    
    async def get_one_shipment(self, db: AsyncSession, shipment_id: int) -> Shipments_Cost:
        result = await db.execute(select(Shipments_Cost).filter(Shipments_Cost.Id_Shipments_Cost == shipment_id))
        return result.scalar_one_or_none()
    
    async def create_shipments_Cost(self, db: AsyncSession, shipments_cost: Shipments_Cost) -> Shipments_Cost:
        db_Shipments_Cost = Shipments_Cost(**shipments_cost.dict())
        db.add(db_Shipments_Cost)
        await db.commit()
        await db.refresh(db_Shipments_Cost)
        return db_Shipments_Cost

    async def update_Shipments_Cost(self, db: AsyncSession, Shipments_Cost_id: int, Shipments_Cost_data: Shipments_Cost) -> Shipments_Cost:
        result = await db.execute(select(Shipments_Cost).filter(Shipments_Cost.Id_Shipments_Cost == Shipments_Cost_id))
        db_Shipments_Cost = result.scalar_one_or_none()
        if db_Shipments_Cost is None:
            return None
        for key, value in Shipments_Cost_data.__dict__.items():
            if hasattr(db_Shipments_Cost, key) and value is not None:
                setattr(db_Shipments_Cost, key, value)
        await db.commit()
        return db_Shipments_Cost
