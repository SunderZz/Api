from sqlalchemy import TIMESTAMP, Column, Integer, ForeignKey, PrimaryKeyConstraint, String
from sqlalchemy.orm import relationship
from database import Base

class Asso_33(Base):
    __tablename__ = 'asso_33'
    __table_args__ = (
        PrimaryKeyConstraint('Id_Users_adresses', 'Id_Preferenceship'),
    )

    Id_Users_adresses = Column(Integer, ForeignKey('Users_adresses.Id_Users_adresses'), nullable=False)
    Id_Preferenceship = Column(Integer, ForeignKey('preferenceship.Id_Preferenceship'), nullable=False)
    users_adresses = relationship("Users_adresses", back_populates="asso_33")
    preferenceship = relationship("Preferenceship", back_populates="asso_33")
