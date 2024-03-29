from sqlalchemy import TIMESTAMP, Boolean, Column, ForeignKey, Integer, String, UniqueConstraint
from database import Base
 
class Payment(Base):
    __tablename__ = 'payment'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    payment_date = Column(TIMESTAMP, nullable=False)
    amount = Column(Integer, nullable=False)
    bills = Column(String(50), nullable=False)
    status = Column(Boolean, nullable=False)
    id_orders = Column(Integer, ForeignKey('orders.id'), nullable=False)

    __table_args__ = (UniqueConstraint('id_orders', name='uix_payment_id_orders'),)