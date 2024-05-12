from sqlalchemy import Column, Integer, ForeignKey, PrimaryKeyConstraint, String
from sqlalchemy.orm import relationship
from database import Base

class Linede(Base):
    __tablename__ = 'linede'
    __table_args__ = (
        PrimaryKeyConstraint('Id_Orders', 'Id_Product'),
    )

    Id_Orders = Column(Integer, ForeignKey('orders.Id_Orders'), nullable=False)
    Id_Product = Column(Integer, ForeignKey('product.Id_Product'), nullable=False)
    qte = Column(String(50), nullable=False)
    orders = relationship("Orders", back_populates="lines")
    product = relationship("Product", back_populates="lines")