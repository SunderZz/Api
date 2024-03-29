from sqlalchemy import Column, ForeignKey, Integer, String
from database import Base
 
class Adresse_Type(Base):
    __tablename__ = 'adresse_type'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    shipment_adresse = Column(String(50))
    adresse_bills = Column(String(50))
    id_users_adresses = Column(Integer, ForeignKey('users_adresses.id'), nullable=False)
    id_users = Column(Integer, ForeignKey('users.id'), nullable=False)
