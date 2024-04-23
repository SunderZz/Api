from sqlalchemy import TIMESTAMP, Boolean, Column, ForeignKey, Integer, String, UniqueConstraint
from database import Base
 
class Payment(Base):
    __tablename__ = 'payment'

    Id_Payments = Column(Integer, primary_key=True, autoincrement=True, index=True)
    Payment_Date = Column(TIMESTAMP, nullable=False)
    Amount = Column(Integer, nullable=False)
    Bills = Column(String(50), nullable=False)
    Status = Column(Boolean, nullable=False)
    Id_orders = Column(Integer, ForeignKey('Orders.Id_Orders'), nullable=False)

    __table_args__ = (UniqueConstraint('Orders.Id_Orders', name='uix_payment_id_orders'),)