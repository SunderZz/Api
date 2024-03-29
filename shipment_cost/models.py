from sqlalchemy import  Column, Integer
from database import Base
 
class Shipments_Cost(Base):
    __tablename__ = 'shipments_cost'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    distance = Column(Integer)
    cost = Column(Integer)

