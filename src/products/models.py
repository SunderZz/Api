from sqlalchemy import Boolean, Column, Integer, String, DECIMAL, TIMESTAMP, ForeignKey
from database import Base
 
class Product(Base):
    __tablename__ = 'product'

    Id_Product  = Column(Integer, primary_key=True, autoincrement=True, index=True)
    Name = Column(String(50), nullable=False)
    Description = Column(String(50))
    Price_ht = Column(DECIMAL(15, 2), nullable=False)
    Active = Column(Boolean, nullable=False)
    Date_activation = Column(TIMESTAMP)
    Date_stop = Column(TIMESTAMP)
    Discount = Column(DECIMAL(5, 2))
    Id_tva = Column(Integer, ForeignKey('Tva.Id_Tva'), nullable=False)