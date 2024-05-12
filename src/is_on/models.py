from sqlalchemy import Column, Integer, ForeignKey, PrimaryKeyConstraint, String
from sqlalchemy.orm import relationship
from database import Base

class Is_On(Base):
    __tablename__ = 'is_on'
    __table_args__ = (
        PrimaryKeyConstraint('Id_Season', 'Id_Product'),
    )

    Id_Season = Column(Integer, ForeignKey('season.Id_Season'), nullable=False)
    Id_Product = Column(Integer, ForeignKey('product.Id_Product'), nullable=False)
    season = relationship("Season", back_populates="is_on")
    product = relationship("Product", back_populates="is_on")