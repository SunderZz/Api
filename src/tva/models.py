from sqlalchemy import Column, Integer, String
from database import Base
from sqlalchemy.orm import relationship

class Tva(Base):
    __tablename__ = 'tva'

    Id_Tva  = Column(Integer, primary_key=True, autoincrement=True, index=True)
    Name = Column(String(50), nullable=False)
    Rate = Column(Integer, nullable=False)
    products = relationship("Product", back_populates="tva")

