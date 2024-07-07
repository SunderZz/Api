import uuid
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from .repository import ProducersRepository
from .schema import ProducersBase, ProducersCreateBase, ProducersModifyBase
from common import model_to_dict
from products.router import create_products
from give.router import create_give
from products.repository import ProductRepository
from products.schema import ProductBase, ProductIdBase
from give.repository import GiveRepository
from give.schema import GiveBase
from is_on.repository import IsOnRepository
from unit.schema import UnitBase
from unit.router import create_unity
from unit.repository import UnitRepository


async def get_producers_service(
    producers_repository: ProducersRepository, db: AsyncSession
) -> list[ProducersBase]:
    producers = await producers_repository.get_producers(db)
    producers_list = [model_to_dict(producer) for producer in producers]
    return [ProducersBase(**producer_dict) for producer_dict in producers_list]


async def get_producer_by_user_service(
    producers: str, producers_repository: ProducersRepository, db: AsyncSession
) -> ProducersBase | None:
    value = await producers_repository.get_producers_query(db, producers)
    if value is None:
        return None
    producer_dict = model_to_dict(value)
    return ProducersBase(**producer_dict)


async def get_user_by_producer_service(
    producers: str, producers_repository: ProducersRepository, db: AsyncSession
) -> ProducersBase | None:
    value = await producers_repository.get_user_query(db, producers)
    if value is None:
        return None
    producer_dict = model_to_dict(value)
    return ProducersBase(**producer_dict)


async def create_producer_service(
    producer: ProducersCreateBase,
    producers_repository: ProducersRepository,
    db: AsyncSession,
) -> ProducersBase:
    unique_id = uuid.uuid4()
    producer.Document = (
        f"http://example.com/documents/{producer.Id_Users}_{unique_id}.pdf"
    )

    new_producer = await producers_repository.create_producers(db, producer)
    producer_dict = model_to_dict(new_producer)
    return ProducersBase(**producer_dict)


async def update_producer_service(
    producer_id: int,
    producer: ProducersModifyBase,
    producer_repository: ProducersRepository,
    db: AsyncSession,
) -> ProducersBase:
    unique_id = uuid.uuid4()
    producer.Document = (
        f"http://example.com/documents/{producer.Id_Users}_{unique_id}.pdf"
    )

    updated_producer = await producer_repository.update_producers(
        db, producer_id, producer
    )
    if updated_producer is None:
        raise HTTPException(status_code=404, detail="producer not found")
    producer_dict = model_to_dict(updated_producer)
    return ProducersBase(**producer_dict)


async def create_product_by_producer_service(
    quantity: int,
    producer_id: int,
    unit: UnitBase,
    season: int,
    products: ProductBase,
    give_repository: GiveRepository,
    unit_repository: UnitRepository,
    is_on_repository: IsOnRepository,
    producers_repository: ProducersRepository,
    products_repository: ProductRepository,
    db: AsyncSession,
) -> ProductIdBase:
    product = await create_products(
        season, products, is_on_repository, products_repository, db
    )
    Timestamp = datetime.now().isoformat()
    given_date_exact = datetime.strptime(Timestamp, "%Y-%m-%dT%H:%M:%S.%f").date()
    unity = await create_unity(unit, unit_repository, db)
    await create_give(
        GiveBase(
            Id_Producers=producer_id,
            Id_Unit=unity.Id_Unit,
            Id_Product=product.Id_Product,
            Quantity=quantity,
            Given_Date=given_date_exact,
        ),
        give_repository,
        db,
    )
    return product
