from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint
from database import Base
 
class Producers(Base):
    __tablename__ = 'producers'

    Id_Producers  = Column(Integer, primary_key=True, autoincrement=True, index=True)
    Document = Column(String(50), nullable=False)
    description = Column(String(50))
    Id_Users = Column(Integer, ForeignKey('users.Id_Users'), nullable=False)
