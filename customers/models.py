from sqlalchemy import Column, ForeignKey, Integer,UniqueConstraint
from database import Base
 
class Customers(Base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    id_users = Column(Integer, ForeignKey('users.id'), nullable=False)

    __table_args__ = (UniqueConstraint('id_users', name='uix_customers_id_users'),)

