from sqlalchemy.orm import Session
from .models import Users_adresses

class UsersAdressesRepository:

    def get_users_adresses(db: Session, user_id: int, users_adresse : Users_adresses)-> Users_adresses:
        return db.query(users_adresse).filter(users_adresse.Id_Users_adresses == user_id).first()
    
    def create_user(db:Session,users_id:int,  user_address: Users_adresses)-> Users_adresses:
        db_user=db.query(user_address).filter(user_address.Id_Users_adresses == users_id).first()
        db_user_address = user_address(**user_address.dict(), user_id=users_id)
        db.add(db_user_address)
        db.commit()
        db.refresh(db_user_address)
        return db_user
