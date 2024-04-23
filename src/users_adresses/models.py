from sqlalchemy import DECIMAL, Column, Integer, String, TIMESTAMP
from database import Base
 
class Users_adresses(Base):
    __tablename__ = 'Users_adresses'

    Id_Users_adresses = Column(Integer, primary_key=True, autoincrement=True, index=True)
    Adresse = Column(String(50), nullable=False)
    Phone = Column(Integer, nullable=False)
    Creation = Column(TIMESTAMP, nullable=False)
    Modification = Column(TIMESTAMP)
    Latitude = Column(DECIMAL(15, 2), nullable=False)
    Longitude = Column(DECIMAL(15, 2), nullable=False)
