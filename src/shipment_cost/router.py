import shipment_cost.models as models
from typing import Annotated
from .schema import ShipmentsCostBase
from fastapi import APIRouter, FastAPI, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from database import engine2, AsyncSessionLocal
from .repository import ShipmentsCostRepository
from common import model_to_dict

router = APIRouter(tags=["shipment_cost"])


@router.get(
    "/shipment_cost/",
    status_code=status.HTTP_200_OK,
    response_model=list[ShipmentsCostBase],
)
async def get_all_shipment(
    shipment_cost_repository: ShipmentsCostRepository = Depends(
        ShipmentsCostRepository
    ),
    db: AsyncSession = Depends(get_db),
) -> list[ShipmentsCostBase]:
    shipments = await shipment_cost_repository.get_shipments_Costs(db)
    shipment_list = [model_to_dict(shipment) for shipment in shipments]
    return [ShipmentsCostBase(**shipment_dict) for shipment_dict in shipment_list]


@router.get("/shipment_cost/{shipment_id}", response_model=ShipmentsCostBase)
async def get_one_shipment(
    shipment_id: int,
    shipment_cost_repository: ShipmentsCostRepository = Depends(
        ShipmentsCostRepository
    ),
    db: AsyncSession = Depends(get_db),
) -> ShipmentsCostBase:
    shipment = await shipment_cost_repository.get_one_shipment(db, shipment_id)
    if shipment is None:
        raise HTTPException(
            status_code=404, detail="shipment not found or attribute not found"
        )
    return ShipmentsCostBase(Distance=shipment.Distance, Cost=shipment.Cost)


@router.post(
    "/shipment_cost/",
    status_code=status.HTTP_201_CREATED,
    response_model=ShipmentsCostBase,
)
async def create_shipment(
    shipment: ShipmentsCostBase,
    shipment_cost_repository: ShipmentsCostRepository = Depends(
        ShipmentsCostRepository
    ),
    db: AsyncSession = Depends(get_db),
) -> ShipmentsCostBase:
    new_shipment = await shipment_cost_repository.create_shipments_Cost(db, shipment)
    shipment_dict = model_to_dict(new_shipment)
    return ShipmentsCostBase(**shipment_dict)


@router.put(
    "/shipment_cost/{shipment_id}",
    status_code=status.HTTP_200_OK,
    response_model=ShipmentsCostBase,
)
async def update_shipment(
    shipment_id: int,
    shipment: ShipmentsCostBase,
    shipment_cost_repository: ShipmentsCostRepository = Depends(
        ShipmentsCostRepository
    ),
    db: AsyncSession = Depends(get_db),
) -> ShipmentsCostBase:
    updated_shipment = await shipment_cost_repository.update_Shipments_Cost(
        db, shipment_id, shipment
    )
    if updated_shipment is None:
        raise HTTPException(status_code=404, detail="shipment not found")
    shipment_dict = model_to_dict(updated_shipment)
    return ShipmentsCostBase(**shipment_dict)
