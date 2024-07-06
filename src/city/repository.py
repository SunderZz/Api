from sqlalchemy.ext.asyncio import AsyncSession
from .models import City
from sqlalchemy.future import select


class CityRepository:
    async def get_city(self, db: AsyncSession) -> list[City]:
        result = await db.execute(select(City))
        return result.scalars().all()

    async def get_city_by_name(self, db: AsyncSession, city: str) -> City:
        result = await db.execute(select(City).filter(City.Name == city))
        return result.scalar_one_or_none()

    async def get_city_by_id(self, db: AsyncSession, city: int) -> City:
        result = await db.execute(select(City).filter(City.Id_City == city))
        return result.scalar_one_or_none()

    async def create_city(self, db: AsyncSession, city: City) -> City:
        db_city = City(**city.dict())
        db.add(db_city)
        await db.commit()
        await db.refresh(db_city)
        return db_city

    async def update_city(
        self, db: AsyncSession, city: int, db_city_data: City
    ) -> City:
        result = await db.execute(select(City).filter(City.Id_City == city))
        db_city = result.scalar_one_or_none()
        if db_city:
            for key, value in db_city_data.__dict__.items():
                if hasattr(db_city, key) and value is not None:
                    setattr(db_city, key, value)
            await db.commit()
        return db_city
