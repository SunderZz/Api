from sqlalchemy import  Column, Integer, String
from database import Base

class City(Base):
    __tablename__ = 'city'

    Id_City = Column(Integer, primary_key=True, autoincrement=True, index=True)
    Name = Column(String(50), nullable=False)