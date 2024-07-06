from sqlalchemy import Column, Integer, String
from database import Base
from sqlalchemy.orm import relationship


class Recipes(Base):
    __tablename__ = "recipes"

    Id_Recipes = Column(Integer, primary_key=True, autoincrement=True, index=True)
    description = Column(String(50))
    Recipe = Column(String(50))
    ingredient = Column(String(50))
    Title = Column(String(50))
    found = relationship("Found", back_populates="recipes")
