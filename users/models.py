from sqlalchemy import Boolean, Column, Integer, String, TIMESTAMP
from database import Base
 

class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    f_name = Column(String(50), nullable=False)
    name = Column(String(50), nullable=False)
    mail = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    creation_date = Column(TIMESTAMP, nullable=False)
    modification_date = Column(TIMESTAMP)
    active = Column(Boolean, nullable=False)