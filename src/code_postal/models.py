from sqlalchemy import Column, Integer
from database import Base
from sqlalchemy.orm import relationship

class Code_Postal(Base):
    __tablename__ = 'code_postal'

    Id_Code_Postal = Column(Integer, primary_key=True, autoincrement=True, index=True)
    code_postal = Column(Integer, nullable=False)
    locate = relationship("Located", back_populates="code_postal")
    got = relationship("Got", back_populates="code_postal")
