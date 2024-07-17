from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from .repository import OrdersRepository
from .schema import OrdersBase, OrdersIdBase,OrdersForBillsBase
from common import model_to_dict
from linede.router import create_linede_for_order, get_linede_by_id
from linede.repository import LinedeRepository
from linede.schema import LinedeBase
from products.router import get_product_by_ids
from products.repository import ProductRepository
from give.router import get_give_by_id, update_give
from give.schema import GiveCalcBase
from give.repository import GiveRepository


async def get_orders_service(
    orders_repository: OrdersRepository, db: AsyncSession
) -> list[OrdersBase]:
    orderss = await orders_repository.get_orders(db)
    orders_list = [model_to_dict(orders) for orders in orderss]
    return [OrdersBase(**orders_dict) for orders_dict in orders_list]


async def get_orders_value_service(
    id_orders: int, orders_repository: OrdersRepository, db: AsyncSession
) -> OrdersBase:
    value = await orders_repository.get_orders_query(db, id_orders)
    if value is None:
        raise HTTPException(
            status_code=404, detail="orders not found or attribute not found"
        )
    orders_dict = model_to_dict(value)
    return OrdersBase(**orders_dict)

async def get_customer_value_service(
    id_casual: int, orders_repository: OrdersRepository, db: AsyncSession
) -> OrdersForBillsBase|list[OrdersForBillsBase]:
    value = await orders_repository.get_all_order_of_customer(db, id_casual)
    if value is None:
        raise HTTPException(
            status_code=404, detail="orders not found or attribute not found"
        )
    if isinstance(value, list):
        orders_list = [model_to_dict(orders) for orders in value]
        return [OrdersForBillsBase(**orders_dict) for orders_dict in orders_list]
    else:
        orders_dict = model_to_dict(value)
        return OrdersForBillsBase(**orders_dict)


async def create_orders_from_user_service(
    orders: OrdersBase, orders_repository: OrdersRepository, db: AsyncSession
) -> OrdersIdBase:
    new_orders = await orders_repository.create_orders(db, orders)
    orders_dict = model_to_dict(new_orders)
    return OrdersIdBase(**orders_dict)


async def update_orders_service(
    orders_id: int,
    orders: OrdersBase,
    orders_repository: OrdersRepository,
    db: AsyncSession,
) -> OrdersBase:
    updated_orders = await orders_repository.update_orders(db, orders_id, orders)
    if updated_orders is None:
        raise HTTPException(status_code=404, detail="orders not found")
    orders_dict = model_to_dict(updated_orders)
    return OrdersBase(**orders_dict)


async def create_orders_card_service(
    casual: OrdersBase,
    products: int | list[int],
    quantity: int | list[int],
    orders_repository: OrdersRepository,
    products_repository: ProductRepository,
    linede_repository: LinedeRepository,
    db: AsyncSession,
) -> OrdersIdBase:
    new_orders = await create_orders_from_user_service(casual, orders_repository, db)
    if isinstance(products, int):
        product_added = await get_product_by_ids(products, products_repository, db)
        for product_in_card in product_added:
            product_id = product_in_card[1]
            created_card = await create_linede_for_order(
                LinedeBase(
                    Id_Orders=new_orders.Id_Orders, Id_Product=product_id, qte=quantity
                ),
                linede_repository,
                db,
            )
    else:
        product_added = []
        for product in products:
            result = await get_product_by_ids(product, products_repository, db)
            product_added.append(result)
        for product_in_card, quantite in zip(product_added, quantity):
            product_id = product_in_card.Id_Product
            created_card = await create_linede_for_order(
                LinedeBase(
                    Id_Orders=new_orders.Id_Orders, Id_Product=product_id, qte=quantite
                ),
                linede_repository,
                db,
            )
    return created_card


async def update_orders_card_service(
    order: int,
    products: int,
    quantity: int,
    products_repository: ProductRepository,
    linede_repository: LinedeRepository,
    db: AsyncSession,
) -> LinedeBase:
    choosen_product = await get_product_by_ids(products, products_repository, db)
    new_product = await create_linede_for_order(
        LinedeBase(
            Id_Orders=order, Id_Product=choosen_product.Id_Product, qte=quantity
        ),
        linede_repository,
        db,
    )
    return new_product


async def valid_orders_card_service(
    order: int,
    id_customers: int,
    give_repository: GiveRepository,
    orders_repository: OrdersRepository,
    linede_repository: LinedeRepository,
    db: AsyncSession,
) -> OrdersBase | list[OrdersBase]:
    Timestamp = datetime.now().isoformat()
    given_date_exact = datetime.strptime(Timestamp, "%Y-%m-%dT%H:%M:%S.%f").date()
    card = await get_linede_by_id(order, linede_repository, db)
    if isinstance(card, list):
        for object in card:
            product = await get_give_by_id(object.Id_Product, give_repository, db)
            updated_quantity = product.Quantity - object.qte
            if updated_quantity < 0:
                raise HTTPException(status_code=403, detail="Capacity not authorize")
            await update_give(
                object.Id_Product,
                GiveCalcBase(
                    Id_Product=object.Id_Product,
                    Quantity=updated_quantity,
                    Given_Date=given_date_exact,
                ),
                give_repository,
                db,
            )
        order_final = await update_orders_service(
            order,
            OrdersBase(
                Command_Date=given_date_exact, Status=False, Id_Casual=id_customers
            ),
            orders_repository,
            db,
        )
        return order_final
    else:
        product = await get_give_by_id(card.Id_Product, give_repository, db)
        updated_quantity = product.Quantity - card.qte
        if updated_quantity < 0:
            raise HTTPException(status_code=403, detail="Capacity not authorize")
        await update_give(
            card.Id_Product,
            GiveCalcBase(
                Id_Product=card.Id_Product,
                Quantity=updated_quantity,
                Given_Date=given_date_exact,
            ),
            give_repository,
            db,
        )
    order_final = await update_orders_service(
        order,
        OrdersBase(Command_Date=given_date_exact, Status=False, Id_Casual=id_customers),
        orders_repository,
        db,
    )
    return order_final
