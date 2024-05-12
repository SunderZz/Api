from sqlalchemy import Column, Integer, ForeignKey, PrimaryKeyConstraint, String
from sqlalchemy.orm import relationship
from database import Base

class Found(Base):
    __tablename__ = 'Found'
    __table_args__ = (
        PrimaryKeyConstraint('Id_Product', 'Id_Recipes'),
    )

    Id_Product = Column(Integer, ForeignKey('product.Id_Product'), nullable=False)
    Id_Recipes = Column(Integer, ForeignKey('recipes.Id_Recipes'), nullable=False)
    product = relationship("Product", back_populates="found")
    recipes = relationship("Recipes", back_populates="found")