from sqlalchemy import  Column, Integer
from database import Base
 
class Shipments_Cost(Base):
    __tablename__ = 'shipments_cost'

    Id_Shipments_Cost  = Column(Integer, primary_key=True, autoincrement=True, index=True)
    Distance = Column(Integer)
    Cost = Column(Integer)

