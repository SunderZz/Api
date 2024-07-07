from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from .repository import ShipmentsCostRepository
from .schema import ShipmentsCostBase
from common import model_to_dict

async def get_all_shipment_costs_service(shipment_cost_repository: ShipmentsCostRepository, db: AsyncSession) -> list[ShipmentsCostBase]:
    shipments = await shipment_cost_repository.get_shipments_Costs(db)
    shipment_list = [model_to_dict(shipment) for shipment in shipments]
    return [ShipmentsCostBase(**shipment_dict) for shipment_dict in shipment_list]

async def get_one_shipment_service(shipment_id: int, shipment_cost_repository: ShipmentsCostRepository, db: AsyncSession) -> ShipmentsCostBase:
    shipment = await shipment_cost_repository.get_one_shipment(db, shipment_id)
    if shipment is None:
        raise HTTPException(
            status_code=404, detail="shipment not found not found"
        )
    return ShipmentsCostBase(Distance=shipment.Distance, Cost=shipment.Cost)

async def create_shipment_service(shipment: ShipmentsCostBase, shipment_cost_repository: ShipmentsCostRepository, db: AsyncSession) -> ShipmentsCostBase:
    new_shipment = await shipment_cost_repository.create_shipments_Cost(db, shipment)
    shipment_dict = model_to_dict(new_shipment)
    return ShipmentsCostBase(**shipment_dict)

async def update_shipment_service(shipment_id: int, shipment: ShipmentsCostBase, shipment_cost_repository: ShipmentsCostRepository, db: AsyncSession) -> ShipmentsCostBase:
    updated_shipment = await shipment_cost_repository.update_Shipments_Cost(db, shipment_id, shipment)
    if updated_shipment is None:
        raise HTTPException(status_code=404, detail="shipment not found")
    shipment_dict = model_to_dict(updated_shipment)
    return ShipmentsCostBase(**shipment_dict)
