from sqlalchemy import Column, Integer, String, TIMESTAMP
from database import Base
from sqlalchemy.orm import relationship

class Notice(Base):
    __tablename__ = 'notice'

    Id_Notice = Column(Integer, primary_key=True, autoincrement=True, index=True)
    Title = Column(String(50))
    Notice = Column(String(50))
    Notice_date = Column(TIMESTAMP, nullable=False)
    Note = Column(Integer, nullable=False)
    given = relationship("Given", back_populates="notice")
    give_1 = relationship("Give_1", back_populates="notice")
