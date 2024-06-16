from sqlalchemy import DECIMAL, Column, Integer, String, TIMESTAMP
from database import Base
from sqlalchemy.orm import relationship
 
class Users_adresses(Base):
    __tablename__ = 'Users_adresses'

    Id_Users_adresses = Column(Integer, primary_key=True, autoincrement=True, index=True)
    Adresse = Column(String(50), nullable=False)
    Phone = Column(String(15), nullable=False)
    Creation = Column(TIMESTAMP, nullable=False)
    Modification = Column(TIMESTAMP)
    Latitude = Column(DECIMAL(15, 2))
    Longitude = Column(DECIMAL(15, 2))
    locate = relationship("Located", back_populates="users_adresses")
    asso_33 = relationship("Asso_33", back_populates="users_adresses")
