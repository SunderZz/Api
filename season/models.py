from sqlalchemy import  Column, Integer, String
from database import Base
 
class Tva(Base):
    __tablename__ = 'tva'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String(50), nullable=False)
    rate = Column(Integer, nullable=False)