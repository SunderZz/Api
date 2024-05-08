from sqlalchemy import Column, ForeignKey, Integer, UniqueConstraint
from database import Base

class Admin(Base):
    __tablename__ = 'admin'

    Id_Admin = Column(Integer, primary_key=True, autoincrement=True, index=True)
    Id_Users = Column(Integer, ForeignKey('users.Id_Users'), nullable=False)
