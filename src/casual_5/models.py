from sqlalchemy import Column, Integer, String
from database import Base
 
class Casual_5(Base):
    __tablename__ = 'casual_5'

    Id_Casual  = Column(Integer, primary_key=True, autoincrement=True, index=True)
    nom = Column(String(50))
