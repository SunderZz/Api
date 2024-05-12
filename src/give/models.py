from sqlalchemy import TIMESTAMP, Column, Integer, ForeignKey, PrimaryKeyConstraint, String
from sqlalchemy.orm import relationship
from database import Base

class Give(Base):
    __tablename__ = 'Give'
    __table_args__ = (
        PrimaryKeyConstraint('Id_Producers', 'Id_Unit', 'Id_Product'),
    )

    Id_Producers = Column(Integer, ForeignKey('producers.Id_Producers'), nullable=False)
    Id_Unit = Column(Integer, ForeignKey('unit.Id_Unit'), nullable=False)
    Id_Product = Column(Integer, ForeignKey('product.Id_Product'), nullable=False)
    Quantity = Column(String(50), nullable=False)
    Given_Date = Column(TIMESTAMP, nullable=False)
    producers = relationship("Producers", back_populates="give")
    unit = relationship("Unit", back_populates="give")
    product = relationship("Product", back_populates="give")