from sqlalchemy import Column, ForeignKey, Integer, String
from database import Base


class Adresse_Type(Base):
    __tablename__ = "adresse_type"

    Id_Adresse_Type = Column(Integer, primary_key=True, autoincrement=True, index=True)
    Shipment_Adresse = Column(String(255))
    Adresse_Bills = Column(String(255))
    Id_Users_adresses = Column(
        Integer, ForeignKey("Users_adresses.Id_Users_adresses"), nullable=False
    )
    Id_Users = Column(Integer, ForeignKey("users.Id_Users"), nullable=False)
