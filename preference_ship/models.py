from sqlalchemy import Column, Integer
from database import Base
 
class Preferenceship(Base):
    __tablename__ = 'preferenceship'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
