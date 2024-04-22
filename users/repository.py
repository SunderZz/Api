from sqlalchemy.orm import Session
from .models import Users


def create_user(db: Session, F_Name: str, name: str, mail: str, password: str) -> Users:
    db_user = Users(F_Name=F_Name, name=name, mail=mail, password=password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_user(db: Session, user: Users):
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user_by_id(db: Session, user_id: int):
    return db.query(Users).filter(Users.id == user_id).first()

def get_all_users(db: Session):
    return db.query(Users).all()

def update_user(db: Session, user: Users):
    db.query(Users).filter(Users.id == user.id).update(user.__dict__)
    db.commit()
    return get_user_by_id(db, user.id)

def delete_user(db: Session, user_id: int):
    db.query(Users).filter(Users.id == user_id).delete()
    db.commit()
