from sqlalchemy.orm import Session
from .models import City

class CityRepository:
    async def get_city(self, db: Session)->list[City]:
        return db.query(City).all()
    
    async def get_city_query(self,db: Session, city: str)->City:
        return db.query(City).filter(City.Name == city).first()  


    async def create_city(self, db: Session, city: City)->City:
        db_city = City(**city.dict())
        db.add(db_city)
        db.commit()
        db.refresh(db_city)
        return db_city

    async def update_city(self, db: Session, city: int, db_city_data: City)->City:
        db_city = db.query(City).filter(City.Id_City == city).first()
        if db_city is None:
            return None
        for key, value in db_city_data.__dict__.items():
            if hasattr(db_city, key) and value is not None:
                setattr(db_city, key, value)
        db.commit()
        return db_city