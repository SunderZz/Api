from sqlalchemy import Column, Integer, String
from database import Base
 
class Season(Base):
    __tablename__ = 'season'

    Id_Season = Column(Integer, primary_key=True, autoincrement=True, index=True)
    Name = Column(String(50), nullable=False)
