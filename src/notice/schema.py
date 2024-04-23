from datetime import date
from pydantic import BaseModel

class NoticeBase(BaseModel):
    title: str |None = None
    notice: str |None = None
    notice_date: date
    note: int