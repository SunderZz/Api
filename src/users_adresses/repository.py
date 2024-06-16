from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from .models import Users_adresses
from sqlalchemy.future import select

class UsersAdressesRepository:

    async def get_user_addresses(self, db: AsyncSession, user_id: int) -> list[Users_adresses]:
        result = await db.execute(select(Users_adresses).filter(Users_adresses.Id_Users_adresses == user_id))
        return result.scalars().all()

    async def create_user_address(self, db: AsyncSession, address: Users_adresses) -> Users_adresses:
        address_data = address.dict(by_alias=True)
        db_address = Users_adresses(**address_data)
        db.add(db_address)
        await db.commit()
        await db.refresh(db_address)
        return db_address

    async def update_user_address(self, db: AsyncSession, address_id: int, address: Users_adresses) -> Users_adresses:
        result = await db.execute(select(Users_adresses).filter(Users_adresses.Id_Users_adresses == address_id))
        user_address = result.scalar_one_or_none()
        if user_address:
            user_address.Adresse = address.Adresse
            user_address.Phone = address.Phone
            user_address.Modification = datetime.now()
            await db.commit()
            await db.refresh(user_address)
        return user_address
