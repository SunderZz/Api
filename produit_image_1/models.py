from sqlalchemy import Column, Integer, String
from database import Base
 
class Produit_Image_1(Base):
    __tablename__ = 'produit_image_1'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    nom = Column(String(50))
    lien_image = Column(String(50))
