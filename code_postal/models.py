from sqlalchemy import Column, Integer
from database import Base
 
class Code_Postal(Base):
    __tablename__ = 'code_postal'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    code_postal = Column(Integer, nullable=False)