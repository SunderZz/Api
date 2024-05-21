import users.models as models
from datetime import datetime
from typing import Annotated
from .schema import AdminBase
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
import main as get_db
from database import engine, SessionLocal
from common import model_to_dict
from .repository import AdminRepository
from users.schema import UserBase
from products.schema import ProductBase
from operate.router import create_operate,update_operate
from operate.schema import OperateBase
from operate.repository import OperateRepository
from carry_on.router import create_carry_on,update_carry_on
from carry_on.schema import CarryOnBase
from carry_on.repository import CarryOnRepository
from manage.router import create_manage,update_manage
from manage.schema import ManageBase
from manage.repository import ManageRepository
from recipes.router import create_recipes,update_recipes
from recipes.schema import RecipesBase
from recipes.repository import RecipesRepository
from redac.router import create_redact,update_redact
from redac.schema import RedactBase
from redac.repository import RedactRepository


def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close_all()

router = APIRouter(tags=["admin"])

models.Base.metadata.create_all(bind=engine)

db_dependency= Annotated[Session, Depends(get_db)]


@router.get("/admin/", status_code=status.HTTP_200_OK, response_model=list[AdminBase],summary="Return all admin")
async def get_admin(admin_repository: AdminRepository = Depends(AdminRepository),db: Session = Depends(get_db))-> list[AdminBase]:
    admin = await admin_repository.get_admin(db)
    admin_list = [model_to_dict(user) for user in admin]
    return [AdminBase(**admin_dict) for admin_dict in admin_list]


@router.get("/admin/{admin}", response_model=AdminBase,summary="Return admin base on his id")
async def get_admin_value(admin: str, admin_repository: AdminRepository = Depends(AdminRepository), db: Session = Depends(get_db)) -> AdminBase:
    value = await admin_repository.get_admin_query(db, admin)
    if value is None:
        raise HTTPException(status_code=404, detail="admin not found or attribute not found")
    admin_dict = model_to_dict(value)
        
    return AdminBase(**admin_dict)


@router.post("/admin/", status_code=status.HTTP_201_CREATED, response_model=AdminBase,summary="Create new admin only accesible from db")
async def create_admin(admin: AdminBase,admin_repository: AdminRepository = Depends(AdminRepository), db: Session = Depends(get_db))-> AdminBase:
    new_admin = await admin_repository.create_admin(db, admin)
    admin_dict = model_to_dict(new_admin) 
    return AdminBase(**admin_dict)

@router.put("/admin/{admin_id}", status_code=status.HTTP_200_OK, response_model=AdminBase,summary="Modify admin base on his id")
async def update_admin(admin_id: int, admin: AdminBase,admin_repository: AdminRepository = Depends(AdminRepository), db: Session = Depends(get_db))-> AdminBase:
    updated_admin = await admin_repository.update_admin(db, admin_id, admin)
    if updated_admin is None:
        raise HTTPException(status_code=404, detail="admin not found")
    admin_dict = model_to_dict(updated_admin) 
    return AdminBase(**admin_dict)

@router.put("/admin/{product_id}/active", status_code=status.HTTP_200_OK,response_model=ProductBase,summary="Modify product")
async def update_product_active_status(product_id: int,admin_id: int, active: bool, repository: AdminRepository = Depends(AdminRepository),manage_repository: ManageRepository = Depends(ManageRepository), db: Session = Depends(get_db))->ProductBase:
    product = await repository.update_product_active_status(db, product_id, active)
    Timestamp = datetime.now().isoformat()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    new_manage = await create_manage(ManageBase(Id_Admin=admin_id, Id_Product=product_id,Date_manage=Timestamp),product_id,manage_repository, db)
    if not new_manage:
        await update_manage(admin_id, ManageBase(Id_Admin=admin_id, Id_Product=product_id,Date_manage=Timestamp), manage_repository, db)

    product_dict = model_to_dict(product) 
    return ProductBase(**product_dict)

@router.put("/admin/{casual_id}/active_state", status_code=status.HTTP_200_OK,response_model=UserBase,summary="Modify active state on casual")
async def update_casual_active_status(casual_id: int,admin_id: int, active: bool, repository: AdminRepository = Depends(AdminRepository),operate_repository: OperateRepository = Depends(OperateRepository), db: Session = Depends(get_db))->UserBase:
    user = await repository.modify_user_active_status(db, casual_id, active)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    new_operate = await create_operate(OperateBase(Id_Admin=admin_id, Id_Casual=casual_id),admin_id,operate_repository, db)
    if not new_operate:
        await update_operate(admin_id, OperateBase(Id_Admin=admin_id, Id_Casual=casual_id), operate_repository, db)

    user_dict = model_to_dict(user) 
    return UserBase(**user_dict)

@router.put("/admin/{id_producers}/active_state", status_code=status.HTTP_200_OK,response_model=UserBase,summary="Modify active state on producers")
async def update_producer_active_status(id_producers: int,admin_id: int, active: bool, repository: AdminRepository = Depends(AdminRepository),carry_on_repository: CarryOnRepository = Depends(CarryOnRepository), db: Session = Depends(get_db))->UserBase:
    user = await repository.modify_user_active_status(db, id_producers, active)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    new_operate = await create_carry_on(CarryOnBase(Id_Admin=admin_id, Id_Producers=id_producers),carry_on_repository, db)
    if not new_operate:
        await update_carry_on(admin_id, CarryOnBase(Id_Admin=admin_id, Id_Producers=id_producers), carry_on_repository, db)

    user_dict = model_to_dict(user) 
    return UserBase(**user_dict)

@router.post("/admin/recipes", status_code=status.HTTP_200_OK,response_model=RecipesBase,summary="Create a new recipes from an admin")
async def create_recipes_from_admin(admin_id: int,recipes: RecipesBase,recipes_repository: RecipesRepository = Depends(RecipesRepository),redac_repository: RedactRepository = Depends(RedactRepository), db: Session = Depends(get_db))->RecipesBase:
    recipes = await recipes_repository.create_Recipes(db, recipes)
    if recipes is None:
        raise HTTPException(status_code=404, detail="recipes not found")
    Id_Recipes = recipes.Id_Recipes
    new_operate = await create_redact(admin_id,Id_Recipes,RedactBase(Id_Admin=admin_id, Id_Recipes=Id_Recipes),redac_repository, db)
    if not new_operate:
        await update_recipes(RedactBase(Id_Admin=admin_id, Id_Recipes=Id_Recipes),Id_Recipes, redac_repository, db)

    return recipes

@router.put("/admin/{id_recipes}/modify_recipes", status_code=status.HTTP_200_OK,response_model=RecipesBase,summary="Modify a new recipes from an admin")
async def update_recipes_from_admin(admin_id: int,id_recipes: int,recipes: RecipesBase,recipes_repository: RecipesRepository = Depends(RecipesRepository),redac_repository: RedactRepository = Depends(RedactRepository), db: Session = Depends(get_db))->RecipesBase:
    recipes = await update_recipes(id_recipes,recipes,recipes_repository, db)
    if recipes is None:
        raise HTTPException(status_code=404, detail="recipes not found")
    new_operate = await create_redact(admin_id,id_recipes,RedactBase(Id_Admin=admin_id, Id_Recipes=id_recipes),redac_repository, db)
    if not new_operate:
        await update_redact(id_recipes, RedactBase(Id_Admin=admin_id, Id_Recipes=id_recipes), redac_repository, db)
    return recipes
