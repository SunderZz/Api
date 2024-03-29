from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint
from database import Base
 
class Producers(Base):
    __tablename__ = 'producers'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    document = Column(String(50), nullable=False)
    description = Column(String(50))
    id_users = Column(Integer, ForeignKey('users.id'), nullable=False)

    __table_args__ = (UniqueConstraint('id_users', name='uix_producers_id_users'),)