import users.models as models
from typing import Annotated
from .schema import AdminBase
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
import main as get_db
from database import engine, SessionLocal
from common import model_to_dict
from .repository import AdminRepository

def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close_all()

router = APIRouter(tags=["admin"])

models.Base.metadata.create_all(bind=engine)

db_dependency= Annotated[Session, Depends(get_db)]


@router.get("/admin/", status_code=status.HTTP_200_OK, response_model=list[AdminBase])
async def get_admin(admin_repository: AdminRepository = Depends(AdminRepository),db: Session = Depends(get_db))-> list[AdminBase]:
    admin = await admin_repository.get_admin(db)
    admin_list = [model_to_dict(user) for user in admin]
    return [AdminBase(**admin_dict) for admin_dict in admin_list]


@router.get("/admin/{admin}", response_model=AdminBase)
async def get_admin_value(admin: str, admin_repository: AdminRepository = Depends(AdminRepository), db: Session = Depends(get_db)) -> AdminBase:
    value = await admin_repository.get_admin_query(db, admin)
    if value is None:
        raise HTTPException(status_code=404, detail="admin not found or attribute not found")
    admin_dict = model_to_dict(value)
        
    return AdminBase(**admin_dict)


@router.post("/admin/", status_code=status.HTTP_201_CREATED, response_model=AdminBase)
async def create_admin(admin: AdminBase,admin_repository: AdminRepository = Depends(AdminRepository), db: Session = Depends(get_db))-> AdminBase:
    new_admin = await admin_repository.create_admin(db, admin)
    admin_dict = model_to_dict(new_admin) 
    return AdminBase(**admin_dict)

@router.put("/admin/{admin_id}", status_code=status.HTTP_200_OK, response_model=AdminBase)
async def update_admin(admin_id: int, admin: AdminBase,admin_repository: AdminRepository = Depends(AdminRepository), db: Session = Depends(get_db))-> AdminBase:
    updated_admin = await admin_repository.update_admin(db, admin_id, admin)
    if updated_admin is None:
        raise HTTPException(status_code=404, detail="admin not found")
    admin_dict = model_to_dict(updated_admin) 
    return AdminBase(**admin_dict)

@router.put("/users/{user_id}/active", status_code=status.HTTP_200_OK)
async def update_user_active_status(user_id: int, active: bool, repository: AdminRepository = Depends(AdminRepository), db: Session = Depends(get_db)):
    user = await repository.update_user_active_status(db, user_id, active)
    return {"message": f"Le statut actif de l'utilisateur {user_id} a été mis à jour avec succès.", "active": user.active}