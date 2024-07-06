from sqlalchemy import Column, ForeignKey, Integer, String
from database import Base
from sqlalchemy.orm import relationship


class Producers(Base):
    __tablename__ = "producers"

    Id_Producers = Column(Integer, primary_key=True, autoincrement=True, index=True)
    Document = Column(String(50), nullable=False)
    description = Column(String(50))
    Id_Users = Column(Integer, ForeignKey("users.Id_Users"), nullable=False)
    give = relationship("Give", back_populates="producers")
    carry = relationship("CarryOn", back_populates="producers")
