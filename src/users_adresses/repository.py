from sqlalchemy.orm import Session
from .models import Users_adresses

class UsersAdressesRepository:

    def get_users_adresses(db: Session, user_id: int, users_adresse : Users_adresses):
        return db.query(users_adresse).filter(users_adresse.Id_Users_adresses == user_id).first()