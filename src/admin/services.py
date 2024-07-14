from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from fastapi import HTTPException
from .schema import AdminBase, AdminCreateBase
from .repository import AdminRepository
from common import model_to_dict
from users.schema import UserBase
from products.schema import ProductBase
from operate.schema import OperateBase
from operate.repository import OperateRepository
from carry_on.schema import CarryOnBase
from carry_on.repository import CarryOnRepository
from manage.schema import ManageBase
from manage.repository import ManageRepository
from recipes.schema import RecipesBase
from recipes.repository import RecipesRepository
from redac.schema import RedactBase
from redac.repository import RedactRepository
from recipes.schema import RecipesCreateBase
from customers.repository import CustomersRepository
from producers.repository import ProducersRepository
from carry_on.router import create_carry_on, get_carry_onose_by_id
from operate.router import create_operate, get_operate_by_id
from manage.router import create_manage
from recipes.router import update_recipes
from redac.router import create_redact, update_redact
from producers.router import get_producer_by_user
from customers.router import get_customer_value


async def get_all_admins_services(
    db: AsyncSession, admin_repository: AdminRepository
) -> list[AdminBase]:
    admins = await admin_repository.get_admin(db)
    return [AdminBase(**model_to_dict(admin)) for admin in admins]


async def get_admin_by_id_services(
    db: AsyncSession, admin_id: str, admin_repository: AdminRepository
) -> AdminBase:
    admin = await admin_repository.get_admin_query(db, admin_id)
    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found")
    return AdminBase(**model_to_dict(admin))


async def create_admin_services(
    db: AsyncSession, admin: AdminCreateBase, admin_repository: AdminRepository
) -> AdminBase:
    new_admin = await admin_repository.create_admin(db, admin)
    return AdminBase(**model_to_dict(new_admin))


async def update_admin_services(
    db: AsyncSession, admin_id: int, admin: AdminBase, admin_repository: AdminRepository
) -> AdminBase:
    updated_admin = await admin_repository.update_admin(db, admin_id, admin)
    if not updated_admin:
        raise HTTPException(status_code=404, detail="Admin not found")
    return AdminBase(**model_to_dict(updated_admin))


async def delete_recipe_service(
    db: AsyncSession,
    admin_id: int,
    recipe_id: int,
    recipe_repository: RecipesRepository,
) -> None:
    if admin_id:
        await recipe_repository.delete_recipe(db, recipe_id)
        return None


async def update_product_active_status_services(
    db: AsyncSession,
    product_id: int,
    active: bool,
    admin_id: int,
    manage_repository: ManageRepository,
    admin_repository: AdminRepository,
) -> ProductBase:
    product = await admin_repository.update_product_active_status(
        db, product_id, active
    )
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    timestamp = datetime.now().isoformat()
    given_date_exact = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%f").date()

    await create_manage(
        ManageBase(
            Id_Admin=admin_id, Id_Product=product_id, Date_manage=given_date_exact
        ),
        product_id,
        manage_repository,
        db,
    )

    return ProductBase(**model_to_dict(product))


async def update_casual_active_status_services(
    db: AsyncSession,
    user_id: int,
    active: bool,
    admin_id: int,
    customer_repository: CustomersRepository,
    operate_repository: OperateRepository,
    admin_repository: AdminRepository,
) -> UserBase:
    user = await admin_repository.modify_user_active_status(db, user_id, active)
    customer = await get_customer_value(user.Id_Users, customer_repository, db)
    id_casual = customer.Id_Casual
    exist_operate = await get_operate_by_id(id_casual, operate_repository, db)

    if not exist_operate:
        await create_operate(
            OperateBase(Id_Admin=admin_id, Id_Casual=id_casual),
            admin_id,
            operate_repository,
            db,
        )

    return UserBase(**model_to_dict(user))


async def update_producer_active_status_services(
    db: AsyncSession,
    id_producers: int,
    active: bool,
    admin_id: int,
    carry_on_repository: CarryOnRepository,
    producer_repository: ProducersRepository,
    admin_repository: AdminRepository,
) -> UserBase:
    producer = await get_producer_by_user(id_producers, producer_repository, db)
    print(producer, "test")
    user = await admin_repository.modify_user_active_status(
        db, producer.Id_Users, active
    )

    timestamp = datetime.now().isoformat()
    given_date_exact = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%f").date()
    id_prod = producer.Id_Producers
    exist_carry_on = await get_carry_onose_by_id(id_prod, carry_on_repository, db)

    if not exist_carry_on:
        await create_carry_on(
            CarryOnBase(
                Id_Admin=admin_id, Id_Producers=id_prod, date_carry=given_date_exact
            ),
            id_prod,
            carry_on_repository,
            db,
        )

    return UserBase(**model_to_dict(user))


async def create_recipes_from_admin_services(
    db: AsyncSession,
    admin_id: int,
    recipes: RecipesCreateBase,
    recipes_repository: RecipesRepository,
    redac_repository: RedactRepository,
) -> RecipesBase:
    new_recipes = await recipes_repository.create_recipe(db, recipes)
    if not new_recipes:
        raise HTTPException(status_code=404, detail="Recipe not found")

    Id_Recipes = new_recipes.Id_Recipes
    new_operate = await create_redact(
        admin_id,
        Id_Recipes,
        RedactBase(Id_Admin=admin_id, Id_Recipes=Id_Recipes),
        redac_repository,
        db,
    )

    if not new_operate:
        await update_recipes(
            RedactBase(Id_Admin=admin_id, Id_Recipes=Id_Recipes),
            Id_Recipes,
            redac_repository,
            db,
        )

    return new_recipes


async def update_recipes_from_admin_services(
    db: AsyncSession,
    admin_id: int,
    id_recipes: int,
    recipes: RecipesBase,
    recipes_repository: RecipesRepository,
    redac_repository: RedactRepository,
    admin_repository: AdminRepository,
) -> RecipesBase:

    updated_recipes = await update_recipes(id_recipes, recipes, recipes_repository, db)
    if not updated_recipes:
        raise HTTPException(status_code=404, detail="Recipes not found")
    print()
    new_operate = await create_redact(
        admin_id,
        id_recipes,
        RedactBase(Id_Admin=admin_id, Id_Recipes=id_recipes),
        redac_repository,
        db,
    )

    if not new_operate:
        await update_redact(
            id_recipes,
            RedactBase(Id_Admin=admin_id, Id_Recipes=id_recipes),
            redac_repository,
            db,
        )

    return updated_recipes
