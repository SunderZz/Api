from sqlalchemy import TIMESTAMP, Column, Integer, ForeignKey, PrimaryKeyConstraint, String
from sqlalchemy.orm import relationship
from database import Base

class CarryOn(Base):
    __tablename__ = 'carry_on'
    __table_args__ = (
        PrimaryKeyConstraint('Id_Producers', 'Id_Admin'),
    )

    Id_Producers = Column(Integer, ForeignKey('producers.Id_Producers'), nullable=False)
    Id_Admin = Column(Integer, ForeignKey('admin.Id_Admin'), nullable=False)
    date_carry = Column(TIMESTAMP)
    admin = relationship("Admin", back_populates="carry")
    producers = relationship("Producers", back_populates="carry")
