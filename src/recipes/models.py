from sqlalchemy import Column, Integer, String
from database import Base
from sqlalchemy.orm import relationship


class Recipes(Base):
    __tablename__ = "recipes"

    Id_Recipes = Column(Integer, primary_key=True, autoincrement=True, index=True)
    description = Column(String(255))
    Recipe = Column(String(255))
    ingredient = Column(String(255))
    Title = Column(String(100))
    found = relationship("Found", back_populates="recipes")
