from sqlalchemy import Column, Integer, ForeignKey, PrimaryKeyConstraint, String
from sqlalchemy.orm import relationship
from database import Base

class Given(Base):
    __tablename__ = 'Given'
    __table_args__ = (
        PrimaryKeyConstraint('Id_Notice', 'Id_Product'),
    )

    Id_Notice = Column(Integer, ForeignKey('notice.Id_Notice'), nullable=False)
    Id_Product = Column(Integer, ForeignKey('product.Id_Product'), nullable=False)
    notice = relationship("Notice", back_populates="given")
    product = relationship("Product", back_populates="given")