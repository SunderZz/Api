from sqlalchemy.orm import Session
from .models import Produit_Image

class ProduitImageRepository:
    async def get_produit_image(self, db: Session)->list[Produit_Image]:
        return db.query(Produit_Image).all()
    
    async def get_produit_image_query(self,db: Session, produit_image: int)->Produit_Image:
        return db.query(Produit_Image).filter(Produit_Image.Id_Produit_Image == produit_image).first()
    
    async def create_produit_image(self, db: Session, produit_image: Produit_Image)->Produit_Image:
        db_produit_image = Produit_Image(**produit_image.dict())
        db.add(db_produit_image)
        db.commit()
        db.refresh(db_produit_image)
        return db_produit_image

    async def update_Produit_Image(self, db: Session, produit_image_id: int, db_produit_image_data: Produit_Image)->Produit_Image:
        db_produit_image = db.query(Produit_Image).filter(Produit_Image.Id_Produit_Image == produit_image_id).first()
        if db_produit_image is None:
            return None
        for key, value in db_produit_image_data.__dict__.items():
            if hasattr(db_produit_image, key) and value is not None:
                setattr(db_produit_image, key, value)
        db.commit()
        return db_produit_image