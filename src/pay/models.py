from sqlalchemy import Column, Integer, Date, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from database import Base

class Pay(Base):
    __tablename__ = 'pay'
    __table_args__ = (
        PrimaryKeyConstraint('Id_Payments', 'Id_Casual'),
    )

    Id_Payments = Column(Integer, ForeignKey('payment.Id_Payments'), nullable=False)
    Id_Casual = Column(Integer, ForeignKey('customers.Id_Casual'), nullable=False)
    Date1 = Column(Date, nullable=False)
    payment = relationship("Payment", back_populates="pays")
    customer = relationship("Customers", back_populates="pays")