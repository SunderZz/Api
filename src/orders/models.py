from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, TIMESTAMP
from database import Base
from sqlalchemy.orm import relationship

class Orders(Base):
    __tablename__ = 'orders'

    Id_Orders  = Column(Integer, primary_key=True, autoincrement=True, index=True)
    Command_Date = Column(TIMESTAMP, nullable=False)
    Status = Column(Boolean, nullable=False)
    Preference_Ship = Column(String(50), nullable=False)
    Ship_Date = Column(TIMESTAMP)
    Id_Casual = Column(Integer, ForeignKey('customers.Id_Casual'), nullable=False)
    lines = relationship("Linede", back_populates="orders")
    asso_34 = relationship("Asso_34", back_populates="asso_34")
