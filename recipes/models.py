from sqlalchemy import Column, Integer, String
from database import Base
 
class Recipes(Base):
    __tablename__ = 'recipes'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    description = Column(String(50)) 
    recipe = Column(String(50)) 
    ingredient = Column(String(50))