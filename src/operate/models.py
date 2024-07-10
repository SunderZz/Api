from sqlalchemy import (
    Column,
    TIMESTAMP,
    Integer,
    ForeignKey,
    PrimaryKeyConstraint,
    func,
)
from sqlalchemy.orm import relationship
from database import Base


class Operate(Base):
    __tablename__ = "operate"
    __table_args__ = (PrimaryKeyConstraint("Id_Admin", "Id_Casual"),)

    Id_Admin = Column(Integer, ForeignKey("admin.Id_Admin"), nullable=False)
    Id_Casual = Column(Integer, ForeignKey("customers.Id_Casual"), nullable=False)
    Date_operate = Column(TIMESTAMP, default=func.now(), nullable=False)
    admin = relationship("Admin", back_populates="operates")
    customer = relationship("Customers", back_populates="operates")
