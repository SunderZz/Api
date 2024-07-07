from database import get_db
from .schema import LinedeBase
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from .repository import LinedeRepository
from .services import (
    get_linedes_service,
    get_linede_by_id_service,
    delete_linede_service,
    create_linede_for_order_service,
    update_linede_service,
)

router = APIRouter(tags=["linede"])


@router.get("/linede/", status_code=status.HTTP_200_OK, response_model=list[LinedeBase])
async def get_linedes(
    linede_repository: LinedeRepository = Depends(LinedeRepository),
    db: AsyncSession = Depends(get_db),
) -> list[LinedeBase]:
    return await get_linedes_service(linede_repository, db)


@router.get(
    "/linede/{linede_id}",
    status_code=status.HTTP_200_OK,
    response_model=LinedeBase | list[LinedeBase],
)
async def get_linede_by_id(
    linede_id: int,
    linede_repository: LinedeRepository = Depends(LinedeRepository),
    db: AsyncSession = Depends(get_db),
) -> LinedeBase | list[LinedeBase]:
    return await get_linede_by_id_service(linede_id, linede_repository, db)


@router.delete(
    "/linede/{order_id}/{product_id}", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_linede(
    order_id: int,
    product_id: int,
    linede_repository: LinedeRepository = Depends(LinedeRepository),
    db: AsyncSession = Depends(get_db),
) -> None:
    await delete_linede_service(order_id, product_id, linede_repository, db)


@router.post(
    "/linede/orders",
    status_code=status.HTTP_201_CREATED,
    response_model=LinedeBase | list[LinedeBase],
)
async def create_linede_for_order(
    linede: LinedeBase | list[LinedeBase],
    linede_repository: LinedeRepository = Depends(LinedeRepository),
    db: AsyncSession = Depends(get_db),
) -> LinedeBase | list[LinedeBase]:
    return await create_linede_for_order_service(linede, linede_repository, db)


@router.put(
    "/linede/{id_orders}/{id_product}",
    status_code=status.HTTP_200_OK,
    response_model=LinedeBase,
)
async def update_linede(
    id_orders: int,
    id_product: int,
    linede: LinedeBase,
    linede_repository: LinedeRepository = Depends(LinedeRepository),
    db: AsyncSession = Depends(get_db),
) -> LinedeBase:
    return await update_linede_service(
        id_orders, id_product, linede, linede_repository, db
    )
