from sqlalchemy.orm import Session
from .models import Notice

class NoticeRepository:
    async def get_notice(self, db: Session)->list[Notice]:
        return db.query(Notice).all()
    
    async def create_notice(self, db: Session, notice: Notice)->Notice:
        db_notice = Notice(**notice.dict())
        db.add(db_notice)
        db.commit()
        db.refresh(db_notice)
        return db_notice