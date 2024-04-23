from sqlalchemy import Column, Integer, String, TIMESTAMP
from database import Base
 
class Notice(Base):
    __tablename__ = 'notice'

    Id_Notice = Column(Integer, primary_key=True, autoincrement=True, index=True)
    Title = Column(String(50))
    Notice = Column(String(50))
    Notice_date = Column(TIMESTAMP, nullable=False)
    Note = Column(Integer, nullable=False)
