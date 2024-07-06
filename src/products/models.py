from sqlalchemy import Boolean, Column, Integer, String, DECIMAL, TIMESTAMP, ForeignKey
from database import Base
from sqlalchemy.orm import relationship


class Product(Base):
    __tablename__ = "product"

    Id_Product = Column(Integer, primary_key=True, autoincrement=True, index=True)
    Name = Column(String(50), nullable=False)
    Description = Column(String(50))
    Price_ht = Column(DECIMAL(15, 2), nullable=False)
    Active = Column(Boolean, nullable=False)
    Date_activation = Column(TIMESTAMP)
    Date_stop = Column(TIMESTAMP)
    Discount = Column(DECIMAL(5, 2))
    Id_tva = Column(Integer, ForeignKey("tva.Id_Tva"), nullable=False)
    tva = relationship("Tva", back_populates="products")
    manages = relationship("Manage", back_populates="product")
    lines = relationship("Linede", back_populates="product")
    is_on = relationship("Is_On", back_populates="product")
    given = relationship("Given", back_populates="product")
    give = relationship("Give", back_populates="product")
    found = relationship("Found", back_populates="product")
    choose = relationship("Choose", back_populates="product")
