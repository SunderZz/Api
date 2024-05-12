from sqlalchemy import Column, Integer, String
from database import Base
from sqlalchemy.orm import relationship

class Season(Base):
    __tablename__ = 'season'

    Id_Season = Column(Integer, primary_key=True, autoincrement=True, index=True)
    Name = Column(String(50), nullable=False)
    is_on = relationship("Is_On", back_populates="season")
