import users.models as models
from typing import Annotated
from .schema import NoticeBase
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from database import engine2, AsyncSessionLocal
from common import model_to_dict
from .repository import NoticeRepository

router = APIRouter(tags=["notice"])

@router.get("/notice/", status_code=status.HTTP_200_OK, response_model=list[NoticeBase])
async def get_notices(notice_repository: NoticeRepository = Depends(NoticeRepository),db:AsyncSession = Depends(get_db))-> list[NoticeBase]:
    notices = await notice_repository.get_notice(db)
    notice_list = [model_to_dict(notice) for notice in notices]
    return [NoticeBase(**notice_dict) for notice_dict in notice_list]

@router.post("/notice/", status_code=status.HTTP_201_CREATED, response_model=NoticeBase)
async def create_notice(notice: NoticeBase,notice_repository: NoticeRepository = Depends(NoticeRepository), db:AsyncSession = Depends(get_db))-> NoticeBase:
    new_notice = await notice_repository.create_notice(db, notice)
    notice_dict = model_to_dict(new_notice) 
    return NoticeBase(**notice_dict)