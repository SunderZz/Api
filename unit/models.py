from sqlalchemy import DECIMAL, Column, Integer
from database import Base
 
class Unit(Base):
    __tablename__ = 'unit'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    kg = Column(DECIMAL(15, 1))
    litre = Column(Integer)
    unit = Column(Integer)
    gramme = Column(Integer)
