from sqlalchemy import Column, Integer, String
from database import Base


class Produit_Image(Base):
    __tablename__ = "produit_image_1"

    Id_Produit_Image = Column(Integer, primary_key=True, autoincrement=True, index=True)
    Nom = Column(String(100))
    lien_image = Column(String(128))
