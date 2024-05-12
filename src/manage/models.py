from sqlalchemy import Column, Date, Integer, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from database import Base

class Manage(Base):
    __tablename__ = 'manage'
    __table_args__ = (
        PrimaryKeyConstraint('Id_Product', 'Id_Admin'),
    )

    Id_Admin = Column(Integer, ForeignKey('admin.Id_Admin'), nullable=False)
    Id_Product = Column(Integer, ForeignKey('product.Id_Product'), nullable=False)
    Date_manage = Column(Date, nullable=False)
    admin = relationship("Admin", back_populates="manages")
    product = relationship("Product", back_populates="manages")