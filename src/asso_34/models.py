from sqlalchemy import (
    TIMESTAMP,
    Column,
    Integer,
    ForeignKey,
    PrimaryKeyConstraint,
    String,
)
from sqlalchemy.orm import relationship
from database import Base


class Asso_34(Base):
    __tablename__ = "asso_34"
    __table_args__ = (PrimaryKeyConstraint("Id_Orders", "Id_Preferenceship"),)

    Id_Orders = Column(Integer, ForeignKey("orders.Id_Orders"), nullable=False)
    Id_Preferenceship = Column(
        Integer, ForeignKey("preferenceship.Id_Preferenceship"), nullable=False
    )
    orders = relationship("Orders", back_populates="asso_34")
    preferenceship = relationship("Preferenceship", back_populates="asso_34")
