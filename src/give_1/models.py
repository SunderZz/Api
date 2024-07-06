from sqlalchemy import Column, Integer, ForeignKey, PrimaryKeyConstraint, String
from sqlalchemy.orm import relationship
from database import Base


class Give_1(Base):
    __tablename__ = "Give_1"
    __table_args__ = (PrimaryKeyConstraint("Id_Notice", "Id_Casual"),)

    Id_Notice = Column(Integer, ForeignKey("notice.Id_Notice"), nullable=False)
    Id_Casual = Column(Integer, ForeignKey("customers.Id_Casual"), nullable=False)
    notice = relationship("Notice", back_populates="give_1")
    customer = relationship("Customers", back_populates="give_1")
