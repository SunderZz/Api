from sqlalchemy import Boolean, Column, Integer, String, TIMESTAMP, func
from database import Base


class Users(Base):
    __tablename__ = 'users'

    Id_Users = Column(Integer, primary_key=True, autoincrement=True, index=True)
    F_Name = Column(String(50), nullable=False)
    Name = Column(String(50), nullable=False)
    Mail = Column(String(50), nullable=False)
    Password = Column(String(50), nullable=False)
    token = Column(String(128), unique=True)
    token_creation_date = Column(TIMESTAMP, default=func.now())
    Creation_date = Column(TIMESTAMP, default=func.now())
    Modification_date = Column(TIMESTAMP)
    active = Column(Boolean, nullable=False)

