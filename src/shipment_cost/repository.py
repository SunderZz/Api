from sqlalchemy.orm import Session
from .models import Shipments_Cost

class ShipmentsCostRepository:
    async def get_shipments_Costs(self, db: Session)->Shipments_Cost:
        return db.query(Shipments_Cost).all()
    
    async def get_one_shipment(self,db: Session, shipment_id: int)->Shipments_Cost:
        return db.query(Shipments_Cost).filter(Shipments_Cost.Id_Shipments_Cost == shipment_id).first()
    
    async def create_shipments_Cost(self, db: Session, shipments_cost: Shipments_Cost)->Shipments_Cost:
        db_Shipments_Cost = Shipments_Cost(**shipments_cost.dict())
        db.add(db_Shipments_Cost)
        db.commit()
        db.refresh(db_Shipments_Cost)
        return db_Shipments_Cost

    async def update_Shipments_Cost(self, db: Session, Shipments_Cost_id: int, Shipments_Cost_data: Shipments_Cost)->Shipments_Cost:
        db_Shipments_Cost = db.query(Shipments_Cost).filter(Shipments_Cost.Id_Shipments_Cost == Shipments_Cost_id).first()
        if db_Shipments_Cost is None:
            return None
        for key, value in Shipments_Cost_data.__dict__.items():
            if hasattr(db_Shipments_Cost, key) and value is not None:
                setattr(db_Shipments_Cost, key, value)
        db.commit()
        return db_Shipments_Cost