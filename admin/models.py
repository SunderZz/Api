from sqlalchemy import Column, ForeignKey, Integer, UniqueConstraint
from database import Base
 
class Admin(Base):
    __tablename__ = 'admin'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    id_users = Column(Integer, ForeignKey('users.id'), nullable=False)

    __table_args__ = (UniqueConstraint('id_users', name='uix_admin_id_users'),)
