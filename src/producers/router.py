import users.models as models
from .schema import ProducersBase, ProducersCreateBase, ProducersModifyBase
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from .repository import ProducersRepository
from .services import (
    get_producers_service,
    get_producer_by_user_service,
    get_user_by_producer_service,
    create_producer_service,
    update_producer_service,
    create_product_by_producer_service,
)
from products.repository import ProductRepository
from products.schema import ProductBase, ProductIdBase
from give.repository import GiveRepository
from is_on.repository import IsOnRepository
from unit.schema import UnitBase
from unit.repository import UnitRepository

router = APIRouter(tags=["producers"])


@router.get(
    "/producers/", status_code=status.HTTP_200_OK, response_model=list[ProducersBase]
)
async def get_producers(
    produit_repository: ProducersRepository = Depends(ProducersRepository),
    db: AsyncSession = Depends(get_db),
) -> list[ProducersBase]:
    return await get_producers_service(produit_repository, db)


@router.get("/producers/{producers}", response_model=ProducersBase | None)
async def get_producer_by_user(
    producers: str,
    producers_repository: ProducersRepository = Depends(ProducersRepository),
    db: AsyncSession = Depends(get_db),
) -> ProducersBase | None:
    return await get_producer_by_user_service(producers, producers_repository, db)


@router.get("/producers_user", response_model=ProducersBase | None)
async def get_user_by_producer(
    producers: str,
    producers_repository: ProducersRepository = Depends(ProducersRepository),
    db: AsyncSession = Depends(get_db),
) -> ProducersBase | None:
    return await get_user_by_producer_service(producers, producers_repository, db)


@router.post(
    "/producers/", status_code=status.HTTP_201_CREATED, response_model=ProducersBase
)
async def create_producer(
    producer: ProducersCreateBase,
    producers_repository: ProducersRepository = Depends(ProducersRepository),
    db: AsyncSession = Depends(get_db),
) -> ProducersBase:
    return await create_producer_service(producer, producers_repository, db)


@router.put(
    "/producers/{producer_id}",
    status_code=status.HTTP_200_OK,
    response_model=ProducersBase,
)
async def update_producer(
    producer_id: int,
    producer: ProducersModifyBase,
    producer_repository: ProducersRepository = Depends(ProducersRepository),
    db: AsyncSession = Depends(get_db),
) -> ProducersBase:
    return await update_producer_service(producer_id, producer, producer_repository, db)


@router.post(
    "/producers/{producer_id}/create_product_by_producer",
    status_code=status.HTTP_201_CREATED,
    response_model=ProductIdBase,
)
async def create_product_by_producer(
    quantity: int,
    producer_id: int,
    unit: UnitBase,
    season: int,
    products: ProductBase,
    give_repository: GiveRepository = Depends(GiveRepository),
    unit_repository: UnitRepository = Depends(UnitRepository),
    is_on_repository: IsOnRepository = Depends(IsOnRepository),
    producers_repository: ProducersRepository = Depends(ProducersRepository),
    products_repository: ProductRepository = Depends(ProductRepository),
    db: AsyncSession = Depends(get_db),
) -> ProductIdBase:
    return await create_product_by_producer_service(
        quantity,
        producer_id,
        unit,
        season,
        products,
        give_repository,
        unit_repository,
        is_on_repository,
        producers_repository,
        products_repository,
        db,
    )
