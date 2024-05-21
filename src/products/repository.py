from sqlalchemy.orm import Session
from .models import Product

class ProductRepository:
    async def get_product(self, db: Session)->list[Product]:
        return db.query(Product).all()
    
    async def get_product_query(self,db: Session, product: int)->Product:
        return db.query(Product).filter(Product.Id_Product == product).first()
    
    async def get_product_id_by_name(self,db: Session, name: str)->Product:
        return db.query(Product).filter(Product.Name == name).all()
    
    async def get_products_by_name(self, db: Session, product_name: str) -> Product | list[Product] | None:
            products = db.query(Product).filter(Product.Name == product_name).all()
            if not products:
                return None
            
            if len(products) == 1:
                return products[0]
            
            return products


    async def create_product(self, db: Session, product: Product)->Product:
        db_product = Product(**product.dict())
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return db_product

    async def update_product(self, db: Session, product: int, db_product_data: Product)->Product:
        db_product = db.query(Product).filter(Product.Id_Product == product).first()
        if db_product is None:
            return None
        for key, value in db_product_data.__dict__.items():
            if hasattr(db_product, key) and value is not None:
                setattr(db_product, key, value)
        db.commit()
        return db_product