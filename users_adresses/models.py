from sqlalchemy import DECIMAL, Column, Integer, String, TIMESTAMP
from database import Base
 
class Users_adresses(Base):
    __tablename__ = 'users_adresses'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    adresse = Column(String(50), nullable=False)
    phone = Column(Integer, nullable=False)
    creation = Column(TIMESTAMP, nullable=False)
    modification = Column(TIMESTAMP)
    latitude = Column(DECIMAL(15, 2), nullable=False)
    longitude = Column(DECIMAL(15, 2), nullable=False)
