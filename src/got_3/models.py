from sqlalchemy import Column, Integer, ForeignKey, PrimaryKeyConstraint, String
from sqlalchemy.orm import relationship
from database import Base

class Got(Base):
    __tablename__ = 'Got_3'
    __table_args__ = (
        PrimaryKeyConstraint('Id_City', 'Id_Code_Postal'),
    )

    Id_City = Column(Integer, ForeignKey('city.Id_City'), nullable=False)
    Id_Code_Postal = Column(Integer, ForeignKey('code_postal.Id_Code_Postal'), nullable=False)
    city = relationship("City", back_populates="got")
    code_postal = relationship("Code_Postal", back_populates="got")