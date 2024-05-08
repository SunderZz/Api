import users.models as models
from typing import Annotated
from .schema import NoticeBase
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
import main as get_db
from database import engine, SessionLocal
from common import model_to_dict
from .repository import NoticeRepository

def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close_all()

router = APIRouter(tags=["notice"])

models.Base.metadata.create_all(bind=engine)

db_dependency= Annotated[Session, Depends(get_db)]

@router.get("/notice/", status_code=status.HTTP_200_OK, response_model=list[NoticeBase])
async def get_notices(notice_repository: NoticeRepository = Depends(NoticeRepository),db: Session = Depends(get_db))-> list[NoticeBase]:
    notices = await notice_repository.get_notice(db)
    notice_list = [model_to_dict(notice) for notice in notices]
    return [NoticeBase(**notice_dict) for notice_dict in notice_list]

@router.post("/notice/", status_code=status.HTTP_201_CREATED, response_model=NoticeBase)
async def create_notice(notice: NoticeBase,notice_repository: NoticeRepository = Depends(NoticeRepository), db: Session = Depends(get_db))-> NoticeBase:
    new_notice = await notice_repository.create_notice(db, notice)
    notice_dict = model_to_dict(new_notice) 
    return NoticeBase(**notice_dict)