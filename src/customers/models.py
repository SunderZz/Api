from sqlalchemy import Column, ForeignKey, Integer,UniqueConstraint
from database import Base
 
class Customers(Base):
    __tablename__ = 'customers'

    Id_Casual = Column(Integer, primary_key=True, autoincrement=True, index=True)
    Id_Users = Column(Integer, ForeignKey('Users.Id_Users'), nullable=False)

    __table_args__ = (UniqueConstraint('Users.Id_Users', name='uix_customers_id_users'),)

