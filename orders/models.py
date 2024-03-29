from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, TIMESTAMP
from database import Base
 
class Orders(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    command_date = Column(TIMESTAMP, nullable=False)
    status = Column(Boolean, nullable=False)
    preference_ship = Column(String(50), nullable=False)
    ship_date = Column(TIMESTAMP)
    id_casual = Column(Integer, ForeignKey('customers.id'), nullable=False)
