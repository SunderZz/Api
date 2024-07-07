import shipment_cost.models as models
from .schema import ShipmentsCostBase
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from .repository import ShipmentsCostRepository
from .services import (
    get_all_shipment_costs_service,
    get_one_shipment_service,
    create_shipment_service,
    update_shipment_service
)

router = APIRouter(tags=["shipment_cost"])

@router.get(
    "/shipment_cost/",
    status_code=status.HTTP_200_OK,
    response_model=list[ShipmentsCostBase],
)
async def get_all_shipment(
    shipment_cost_repository: ShipmentsCostRepository = Depends(ShipmentsCostRepository),
    db: AsyncSession = Depends(get_db),
) -> list[ShipmentsCostBase]:
    return await get_all_shipment_costs_service(shipment_cost_repository, db)

@router.get("/shipment_cost/{shipment_id}", response_model=ShipmentsCostBase)
async def get_one_shipment(
    shipment_id: int,
    shipment_cost_repository: ShipmentsCostRepository = Depends(ShipmentsCostRepository),
    db: AsyncSession = Depends(get_db),
) -> ShipmentsCostBase:
    return await get_one_shipment_service(shipment_id, shipment_cost_repository, db)

@router.post(
    "/shipment_cost/",
    status_code=status.HTTP_201_CREATED,
    response_model=ShipmentsCostBase,
)
async def create_shipment(
    shipment: ShipmentsCostBase,
    shipment_cost_repository: ShipmentsCostRepository = Depends(ShipmentsCostRepository),
    db: AsyncSession = Depends(get_db),
) -> ShipmentsCostBase:
    return await create_shipment_service(shipment, shipment_cost_repository, db)

@router.put(
    "/shipment_cost/{shipment_id}",
    status_code=status.HTTP_200_OK,
    response_model=ShipmentsCostBase,
)
async def update_shipment(
    shipment_id: int,
    shipment: ShipmentsCostBase,
    shipment_cost_repository: ShipmentsCostRepository = Depends(ShipmentsCostRepository),
    db: AsyncSession = Depends(get_db),
) -> ShipmentsCostBase:
    return await update_shipment_service(shipment_id, shipment, shipment_cost_repository, db)
