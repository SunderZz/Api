import users.models as models
from typing import Annotated
from .schema import AdminBase
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
import main as get_db
from database import engine, SessionLocal
from common import model_to_dict
from .repository import AdminRepository
from users.schema import UserBase
from operate.router import create_operate,update_operate
from operate.schema import OperateBase
from operate.repository import OperateRepository
from carry_on.router import create_carry_on,update_carry_on
from carry_on.schema import CarryOnBase
from carry_on.repository import CarryOnRepository


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

@router.put("/users/{casual_id}/active", status_code=status.HTTP_200_OK)
async def update_casual_active_status(casual_id: int,admin_id: int, active: bool, repository: AdminRepository = Depends(AdminRepository),operate_repository: OperateRepository = Depends(OperateRepository), db: Session = Depends(get_db))->UserBase:
    user = await repository.update_user_active_status(db, casual_id, active)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    new_operate = await create_operate(OperateBase(Id_Admin=admin_id, Id_Casual=casual_id),admin_id,operate_repository, db)
    if not new_operate:
        await update_operate(admin_id, OperateBase(Id_Admin=admin_id, Id_Casual=casual_id), operate_repository, db)

    user_dict = model_to_dict(user) 
    return UserBase(**user_dict)

@router.put("/users/{producers_id}/active", status_code=status.HTTP_200_OK)
async def update_producer_active_status(producers_id: int,admin_id: int, active: bool, repository: AdminRepository = Depends(AdminRepository),carry_on_repository: CarryOnRepository = Depends(CarryOnRepository), db: Session = Depends(get_db))->UserBase:
    user = await repository.update_user_active_status(db, producers_id, active)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    new_operate = await create_carry_on(CarryOnBase(Id_Admin=admin_id, Id_Producers=producers_id),carry_on_repository, db)
    if not new_operate:
        await update_carry_on(admin_id, CarryOnBase(Id_Admin=admin_id, Id_Producers=producers_id), carry_on_repository, db)

    user_dict = model_to_dict(user) 
    return UserBase(**user_dict)
