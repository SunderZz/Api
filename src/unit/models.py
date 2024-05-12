from sqlalchemy import DECIMAL, Column, Integer
from database import Base
from sqlalchemy.orm import relationship

class Unit(Base):
    __tablename__ = 'unit'

    Id_Unit  = Column(Integer, primary_key=True, autoincrement=True, index=True)
    Kg = Column(DECIMAL(15, 1))
    Litre = Column(Integer)
    Unit = Column(Integer)
    Gramme = Column(Integer)
    give = relationship("Give", back_populates="unit")
