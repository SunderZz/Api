from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from .repository import LinedeRepository
from .schema import LinedeBase
from common import model_to_dict


async def get_linedes_service(
    linede_repository: LinedeRepository, db: AsyncSession
) -> list[LinedeBase]:
    linedes = await linede_repository.get_linede(db)
    linedes_list = [model_to_dict(linede) for linede in linedes]
    return [LinedeBase(**linede_dict) for linede_dict in linedes_list]


async def get_linede_by_id_service(
    linede_id: int, linede_repository: LinedeRepository, db: AsyncSession
) -> LinedeBase | list[LinedeBase]:
    linede = await linede_repository.get_linede_by_id(db, linede_id)
    if linede is None:
        raise HTTPException(status_code=404, detail="Linede not found")
    if isinstance(linede, list):
        linedes_list = [model_to_dict(line) for line in linede]
        return [LinedeBase(**linede_dict) for linede_dict in linedes_list]
    else:
        return LinedeBase(**model_to_dict(linede))


async def delete_linede_service(
    order_id: int,
    product_id: int,
    linede_repository: LinedeRepository,
    db: AsyncSession,
) -> None:
    await linede_repository.delete_linede(db, order_id, product_id)


async def create_linede_for_order_service(
    linede: LinedeBase | list[LinedeBase],
    linede_repository: LinedeRepository,
    db: AsyncSession,
) -> LinedeBase | list[LinedeBase]:
    new_linede = await linede_repository.add_products_to_order(db, linede)
    if isinstance(new_linede, list):
        linedes_list = [model_to_dict(linede) for linede in new_linede]
        return [LinedeBase(**linede_dict) for linede_dict in linedes_list]
    else:
        return LinedeBase(**model_to_dict(new_linede))


async def update_linede_service(
    id_orders: int,
    id_product: int,
    linede: LinedeBase,
    linede_repository: LinedeRepository,
    db: AsyncSession,
) -> LinedeBase:
    updated_linede = await linede_repository.update_linede(
        db, id_orders, id_product, linede
    )
    if updated_linede is None:
        raise HTTPException(status_code=404, detail="Linede not found")
    return LinedeBase(**model_to_dict(updated_linede))
