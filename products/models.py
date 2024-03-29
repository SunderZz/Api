from sqlalchemy import Boolean, Column, Integer, String, DECIMAL, TIMESTAMP, ForeignKey
from database import Base
 
class Product(Base):
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String(50), nullable=False)
    description = Column(String(50))
    price_ht = Column(DECIMAL(15, 2), nullable=False)
    active = Column(Boolean, nullable=False)
    date_activation = Column(TIMESTAMP)
    date_stop = Column(TIMESTAMP)
    discount = Column(DECIMAL(5, 2))
    id_tva = Column(Integer, ForeignKey('tva.id'), nullable=False)