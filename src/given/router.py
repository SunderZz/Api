import season.models as models
from database import get_db
from typing import Annotated
from .schema import GivenBase
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import engine2, AsyncSessionLocal
from .repository import GivenRepository
from common import model_to_dict
from notice.repository import NoticeRepository
from notice.router import create_notice,get_notices_by_id
from notice.schema import NoticeBase
from give_1.repository import Give_1Repository
from give_1.router import create_Give_notice
from give_1.schema import Give_1Base

router = APIRouter(tags=["given"])

@router.get("/given/", status_code=status.HTTP_200_OK, response_model=list[GivenBase])
async def get_givens(given_repository: GivenRepository = Depends(GivenRepository), db:AsyncSession = Depends(get_db)) -> list[GivenBase]:
    givens = await given_repository.get_given(db)
    givens_list = [model_to_dict(given) for given in givens]
    return [GivenBase(**given_dict) for given_dict in givens_list]

@router.get("/given/{given_id}", status_code=status.HTTP_200_OK, response_model=GivenBase)
async def get_given_by_id(given_id: int, given_repository: GivenRepository = Depends(GivenRepository), db:AsyncSession = Depends(get_db)) -> GivenBase:
    given = await given_repository.get_given_by_id(db, given_id)
    if given is None:
        raise HTTPException(status_code=404, detail="given not found")
    return GivenBase(**model_to_dict(given))

@router.get("/get_notice_by_id", status_code=status.HTTP_200_OK, response_model=NoticeBase | list[NoticeBase] | None )
async def get_given_by_id(product: int, given_repository: GivenRepository = Depends(GivenRepository),notice_repository: NoticeRepository = Depends(NoticeRepository), db:AsyncSession = Depends(get_db)) -> NoticeBase | list[NoticeBase] |None:
    given = await given_repository.get_notice_by_product(db, product)
    
    if given is None:
        return None

    if isinstance(given, list):
        notices = []
        for giv in given:
            notice = await get_notices_by_id(giv.Id_Notice, notice_repository, db)
            if notice:
                notices.append(notice)
        return notices if notices else None

    return await get_notices_by_id(given.Id_Notice, notice_repository, db)
    return result

async def get_notices_by_id(
    notice_id: int,
    notice_repository: NoticeRepository,
    db: AsyncSession
) -> NoticeBase:
    notice = await notice_repository.get_notice_by_id(db, notice_id)
    if notice:
        notice_dict = model_to_dict(notice)
        return NoticeBase(**notice_dict)
    raise HTTPException(status_code=404, detail="Notice not found")

@router.post("/given/", status_code=status.HTTP_201_CREATED, response_model=GivenBase)
async def create_notice_for_product(id_customer:int,notice:NoticeBase,product: int, given_repository: GivenRepository = Depends(GivenRepository),Give_1_repository: Give_1Repository = Depends(Give_1Repository), notice_repository: NoticeRepository = Depends(NoticeRepository), db:AsyncSession = Depends(get_db)) -> GivenBase:
    notice_posted = await create_notice(notice, notice_repository, db)
    new_given = await given_repository.create_given(db, GivenBase(Id_Notice=notice_posted.Id_Notice,Id_Product=product))
    await create_Give_notice(Give_1Base(Id_Casual=id_customer,Id_Notice=new_given.Id_Notice),Give_1_repository,db)
    given_dict = model_to_dict(new_given)
    return GivenBase(**given_dict)

@router.put("/given/{given_id}", status_code=status.HTTP_200_OK, response_model=GivenBase)
async def update_given(given_id: int, given: GivenBase, given_repository: GivenRepository = Depends(GivenRepository), db:AsyncSession = Depends(get_db)) -> GivenBase:
    updated_given = await given_repository.update_given(db, given_id, given)
    if updated_given is None:
        raise HTTPException(status_code=404, detail="given not found")
    given_dict = model_to_dict(updated_given)
    return GivenBase(**given_dict)
