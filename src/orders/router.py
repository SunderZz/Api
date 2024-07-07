from .schema import OrdersBase, OrdersIdBase
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from .repository import OrdersRepository
from .services import (
    get_orders_service,
    get_orders_value_service,
    create_orders_from_user_service,
    create_orders_card_service,
    update_orders_card_service,
    valid_orders_card_service,
)
from linede.repository import LinedeRepository
from linede.schema import LinedeBase
from products.repository import ProductRepository
from give.repository import GiveRepository

router = APIRouter(tags=["orders"])


@router.get("/orders/", status_code=status.HTTP_200_OK, response_model=list[OrdersBase])
async def get_orders(
    orders_repository: OrdersRepository = Depends(OrdersRepository),
    db: AsyncSession = Depends(get_db),
) -> list[OrdersBase]:
    return await get_orders_service(orders_repository, db)


@router.get("/orders_by_id/", response_model=OrdersBase)
async def get_orders_value(
    id_orders: int,
    orders_repository: OrdersRepository = Depends(OrdersRepository),
    db: AsyncSession = Depends(get_db),
) -> OrdersBase:
    return await get_orders_value_service(id_orders, orders_repository, db)


@router.post(
    "/orders/", status_code=status.HTTP_201_CREATED, response_model=OrdersIdBase
)
async def create_orders_from_user(
    orders: OrdersBase,
    orders_repository: OrdersRepository = Depends(OrdersRepository),
    db: AsyncSession = Depends(get_db),
) -> OrdersIdBase:
    return await create_orders_from_user_service(orders, orders_repository, db)


@router.post(
    "/orders/card", status_code=status.HTTP_201_CREATED, response_model=OrdersIdBase
)
async def create_orders_card(
    casual: OrdersBase,
    products: int | list[int],
    quantity: int | list[int],
    orders_repository: OrdersRepository = Depends(OrdersRepository),
    products_repository: ProductRepository = Depends(ProductRepository),
    linede_repository: LinedeRepository = Depends(LinedeRepository),
    db: AsyncSession = Depends(get_db),
) -> OrdersIdBase:
    return await create_orders_card_service(
        casual,
        products,
        quantity,
        orders_repository,
        products_repository,
        linede_repository,
        db,
    )


@router.put(
    "/update_order/", status_code=status.HTTP_201_CREATED, response_model=LinedeBase
)
async def update_orders_card(
    order: int,
    products: int,
    quantity: int,
    products_repository: ProductRepository = Depends(ProductRepository),
    linede_repository: LinedeRepository = Depends(LinedeRepository),
    db: AsyncSession = Depends(get_db),
) -> LinedeBase:
    return await update_orders_card_service(
        order, products, quantity, products_repository, linede_repository, db
    )


@router.put(
    "/valid_order/",
    status_code=status.HTTP_201_CREATED,
    response_model=OrdersBase | list[OrdersBase],
)
async def valid_orders_card(
    order: int,
    id_customers: int,
    give_repository: GiveRepository = Depends(GiveRepository),
    orders_repository: OrdersRepository = Depends(OrdersRepository),
    linede_repository: LinedeRepository = Depends(LinedeRepository),
    db: AsyncSession = Depends(get_db),
) -> OrdersBase | list[OrdersBase]:
    return await valid_orders_card_service(
        order, id_customers, give_repository, orders_repository, linede_repository, db
    )
