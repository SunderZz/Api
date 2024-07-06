from sqlalchemy import Column, ForeignKey, Integer
from database import Base
from sqlalchemy.orm import relationship


class Admin(Base):
    __tablename__ = "admin"

    Id_Admin = Column(Integer, primary_key=True, autoincrement=True, index=True)
    Id_Users = Column(Integer, ForeignKey("users.Id_Users"), nullable=False)
    operates = relationship("Operate", back_populates="admin")
    manages = relationship("Manage", back_populates="admin")
    carry = relationship("CarryOn", back_populates="admin")
