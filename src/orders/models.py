from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, TIMESTAMP
from database import Base
 
class Orders(Base):
    __tablename__ = 'orders'

    Id_Orders  = Column(Integer, primary_key=True, autoincrement=True, index=True)
    Command_Date = Column(TIMESTAMP, nullable=False)
    Status = Column(Boolean, nullable=False)
    Preference_Ship = Column(String(50), nullable=False)
    Ship_Date = Column(TIMESTAMP)
    Id_Casual = Column(Integer, ForeignKey('Customers.Id_Casual'), nullable=False)
