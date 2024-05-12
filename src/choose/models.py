from sqlalchemy import Column, Integer, ForeignKey, PrimaryKeyConstraint, String
from sqlalchemy.orm import relationship
from database import Base

class Choose(Base):
    __tablename__ = 'Choose'
    __table_args__ = (
        PrimaryKeyConstraint('Id_Product', 'Id_Casual'),
    )

    Id_Product = Column(Integer, ForeignKey('product.Id_Product'), nullable=False)
    Id_Casual = Column(Integer, ForeignKey('customers.Id_Casual'), nullable=False)
    product = relationship("Product", back_populates="choose")
    customer = relationship("Customers", back_populates="choose")