from sqlalchemy import Column, Integer, String, TIMESTAMP
from database import Base
 
class Notice(Base):
    __tablename__ = 'notice'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    title = Column(String(50))
    notice = Column(String(50))
    notice_date = Column(TIMESTAMP, nullable=False)
    note = Column(Integer, nullable=False)
