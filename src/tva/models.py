from sqlalchemy import Column, Integer, String
from database import Base
 
class Tva(Base):
    __tablename__ = 'tva'

    Id_Tva  = Column(Integer, primary_key=True, autoincrement=True, index=True)
    Name = Column(String(50), nullable=False)
    Rate = Column(Integer, nullable=False)

