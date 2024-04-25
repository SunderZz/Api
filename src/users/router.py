import users.models as models
import main as get_db
from typing import Annotated
from .schema import UserBase
from fastapi import APIRouter,  Depends, HTTPException
from sqlalchemy.orm import Session
from database import engine, SessionLocal
from .repository import UsersRepository
from common import model_to_dict

def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close_all()

router = APIRouter(tags=["users"])

models.Base.metadata.create_all(bind=engine)

db_dependency= Annotated[Session, Depends(get_db)]

@router.get("/users/{user_id}", response_model=UserBase)
async def get_user( user_id: int, user_repository: UsersRepository = Depends(UsersRepository), db: Session = Depends(get_db))-> UserBase:
    user = await user_repository.get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    user_dict = model_to_dict(user) 
    return UserBase(**user_dict)

@router.get("/users", response_model=list[UserBase])
async def get_users(user_repository: UsersRepository = Depends(UsersRepository), db: Session = Depends(get_db)) -> list[UserBase]:
    users = await user_repository.get_all_users(db)
    users_dict = [model_to_dict(user) for user in users]
    return [UserBase(**user_dict) for user_dict in users_dict]

    
@router.post("/users/", response_model=UserBase)
async def create_user(user: UserBase,user_repository: UsersRepository = Depends(UsersRepository), db: Session = Depends(get_db))->UserBase:
    user_post = await user_repository.create_user(db, user)
    user_dict =model_to_dict(user_post)
    return UserBase(**user_dict)

@router.put("/users/{user_id}", response_model=UserBase)
async def update_user(user_id: int,user_data: UserBase, user_repository: UsersRepository = Depends(UsersRepository), db: Session = Depends(get_db))-> UserBase:
    user_put = await user_repository.update_user(db, user_id, user_data)
    if user_put is None:
        raise HTTPException(status_code=404, detail="User not found")
    user_dict = model_to_dict(user_put)
    return UserBase(**user_dict)