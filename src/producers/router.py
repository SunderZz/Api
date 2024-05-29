from datetime import datetime
import users.models as models
from typing import Annotated
from .schema import ProducersBase
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from database import engine2, AsyncSessionLocal
from common import model_to_dict
from .repository import ProducersRepository
from products.router import create_products
from give.router import create_give
from products.repository import ProductRepository
from products.schema import ProductBase
from give.repository import GiveRepository
from products.schema import ProductIdBase
from give.schema import GiveBase
from is_on.repository import IsOnRepository
from unit.schema import UnitBase
from unit.router import create_unity
from unit.repository import UnitRepository


router = APIRouter(tags=["producers"])

@router.get("/producers/", status_code=status.HTTP_200_OK, response_model=list[ProducersBase])
async def get_producers(produit_repository: ProducersRepository = Depends(ProducersRepository),db:AsyncSession = Depends(get_db))-> list[ProducersBase]:
    producers = await produit_repository.get_producers(db)
    producers_list = [model_to_dict(producer) for producer in producers]
    return [ProducersBase(**producer_dict) for producer_dict in producers_list]


@router.get("/producers/{producers}", response_model=ProducersBase)
async def get_producer_value(producers: str, producers_repository: ProducersRepository = Depends(ProducersRepository), db:AsyncSession = Depends(get_db)) -> ProducersBase:
    value = await producers_repository.get_producers_query(db, producers)
    if value is None:
        raise HTTPException(status_code=404, detail="producer not found or attribute not found")
    producer_dict = model_to_dict(value)
        
    return ProducersBase(**producer_dict)


@router.post("/producers/", status_code=status.HTTP_201_CREATED, response_model=ProducersBase)
async def create_producer(producer: ProducersBase,producers_repository: ProducersRepository = Depends(ProducersRepository), db:AsyncSession = Depends(get_db))-> ProducersBase:
    new_producer = await producers_repository.create_producers(db, producer)
    producer_dict = model_to_dict(new_producer) 
    return ProducersBase(**producer_dict)

@router.put("/producers/{producer_id}", status_code=status.HTTP_200_OK, response_model=ProducersBase)
async def update_producer(producer_id: int, producer: ProducersBase,producer_repository: ProducersRepository = Depends(ProducersRepository), db:AsyncSession = Depends(get_db))-> ProducersBase:
    updated_producer = await producer_repository.update_producers(db, producer_id, producer)
    if updated_producer is None:
        raise HTTPException(status_code=404, detail="produit_image not found")
    produit_image_dict = model_to_dict(updated_producer) 
    return ProducersBase(**produit_image_dict)

@router.post("/producers/{producer_id}/create_product_by_producer", status_code=status.HTTP_201_CREATED, response_model=ProductIdBase)
async def create_product_by_producer(quantity:int,producer_id: int,unit:UnitBase,season:int,products:ProductBase,give_repository: GiveRepository = Depends(GiveRepository),unit_repository: UnitRepository = Depends(UnitRepository),is_on_repository: IsOnRepository = Depends(IsOnRepository),producers_repository: ProducersRepository = Depends(ProducersRepository),products_repository: ProductRepository = Depends(ProductRepository), db:AsyncSession = Depends(get_db))-> ProductIdBase:
    product = await create_products(season,products,is_on_repository,products_repository,db)
    Timestamp = datetime.now().isoformat()
    given_date_exact = datetime.strptime(Timestamp, "%Y-%m-%dT%H:%M:%S.%f").date()
    unity = await create_unity(unit,unit_repository,db)
    await create_give(GiveBase(Id_Producers=producer_id,Id_Unit=unity.Id_Unit,Id_Product=product.Id_Product,Quantity=quantity,Given_Date=given_date_exact), give_repository,db)
    return product