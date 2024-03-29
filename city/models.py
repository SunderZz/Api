from sqlalchemy import  Column, Integer, String
from database import Base
 
class City(Base):
    __tablename__ = 'city'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String(50), nullable=False)