from sqlalchemy import Column, ForeignKey, Integer, UniqueConstraint
from database import Base

class Admin(Base):
    __tablename__ = 'admin'

    Id_Admin = Column(Integer, primary_key=True, autoincrement=True, index=True)
    Id_users = Column(Integer, ForeignKey('Users.Id_Users'), nullable=False)

    __table_args__ = (UniqueConstraint('Users.Id_Users', name='uix_admin_id_users'),)
