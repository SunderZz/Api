from datetime import datetime
from sqlalchemy.orm import Session
from .models import Users_adresses

class UsersAdressesRepository:

    async def get_user_addresses(db: Session, user_id: int) -> list[Users_adresses]:
        return db.query(Users_adresses).filter(Users_adresses.Id_Users_adresses == user_id).all()


    async def create_user_address(db: Session, address: Users_adresses) -> Users_adresses:
        address_data = address.dict(by_alias=True)
        db_address = Users_adresses(**address_data)
        db.add(db_address)
        db.commit()
        db.refresh(db_address)
        return db_address


    async def update_user_address(db: Session, address_id: int, address: Users_adresses) -> Users_adresses:
        user_address = db.query(Users_adresses).filter(Users_adresses.Id_Users_adresses == address_id).first()
        user_address.Adresse = address.Adresse
        user_address.Phone = address.Phone
        user_address.Creation = address.Creation
        user_address.Modification = datetime.now()
        user_address.Latitude = address.Latitude
        user_address.Longitude = address.Longitude
        db.commit()
        return user_address
