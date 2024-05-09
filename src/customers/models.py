from sqlalchemy import Column, ForeignKey, Integer
from database import Base
from sqlalchemy.orm import relationship

class Customers(Base):
    __tablename__ = 'customers'

    Id_Casual = Column(Integer, primary_key=True, autoincrement=True, index=True)
    Id_Users = Column(Integer, ForeignKey('users.Id_Users'), nullable=False)
    pays = relationship("Pay", back_populates="customer")