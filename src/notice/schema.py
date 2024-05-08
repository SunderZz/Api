from datetime import date
from pydantic import BaseModel

class NoticeBase(BaseModel):
    Title: str |None = None
    Notice: str |None = None
    Notice_date: date
    Note: int