from sqlalchemy import Column, Integer
from database import Base
from sqlalchemy.orm import relationship


class Preferenceship(Base):
    __tablename__ = "preferenceship"

    Id_Preferenceship = Column(
        Integer, primary_key=True, autoincrement=True, index=True
    )
    asso_33 = relationship("Asso_33", back_populates="preferenceship")
    asso_34 = relationship("Asso_34", back_populates="preferenceship")
