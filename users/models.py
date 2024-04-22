from sqlalchemy import Boolean, Column, Integer, String, TIMESTAMP, func
from database import Base
 

class Users(Base):
    __tablename__ = 'users'

    Id_Users = Column(Integer, primary_key=True, autoincrement=True, index=True)
    F_Name = Column(String(50), nullable=False)
    name = Column(String(50), nullable=False)
    mail = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    creation_date = Column(TIMESTAMP, default=func.now())
    modification_date = Column(TIMESTAMP)
