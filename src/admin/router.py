import admin.models as models
from typing import Annotated
from .schema import AdminBase
from fastapi import APIRouter, FastAPI, Depends, status
from sqlalchemy.orm import Session
import main as get_db
from database import engine, AsyncSessionLocal


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

router = APIRouter(tags=["admin"])

models.Base.metadata.create_all(bind=engine)

db_dependency= Annotated[Session, Depends(get_db)]


@router.get("/admin/", status_code= status.HTTP_201_CREATED)
async def get_admin(db: db_dependency):
    admin= db.query(models.Admin).all()
    return {"admin":admin}

@router.get("/admin_name/", status_code=status.HTTP_200_OK)
async def get_admin(db: Session = Depends(get_db)):
    admins = db.query(models.Admin).all()
    admin_data = []
    for admin in admins:
        user_data = {
            "id_users": admin.id_users,
            "first_name": admin.user.first_name,
            "name": admin.user.name
        }
        admin_data.append(user_data)
    return {"admin": admin_data}