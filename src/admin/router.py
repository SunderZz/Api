from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from .schema import AdminBase, AdminCreateBase
from .repository import AdminRepository
from .services import AdminService
from users.schema import UserBase
from products.schema import ProductBase
from carry_on.repository import CarryOnRepository
from manage.repository import ManageRepository
from customers.repository import CustomersRepository
from producers.repository import ProducersRepository
from recipes.repository import RecipesRepository
from redac.repository import RedactRepository
from operate.repository import OperateRepository
from recipes.schema import RecipesBase

router = APIRouter(tags=["admin"])


def get_service(
    admin_repository: AdminRepository = Depends(AdminRepository),
) -> AdminService:
    return AdminService(admin_repository)


@router.get(
    "/admin/",
    status_code=status.HTTP_200_OK,
    response_model=list[AdminBase],
    summary="Return all admins",
)
async def get_admin(
    db: AsyncSession = Depends(get_db), service: AdminService = Depends(get_service)
) -> list[AdminBase]:
    return await service.get_all_admins(db)


@router.get(
    "/admin/{admin_id}",
    status_code=status.HTTP_200_OK,
    response_model=AdminBase,
    summary="Return admin by id",
)
async def get_admin_value(
    admin_id: str,
    db: AsyncSession = Depends(get_db),
    service: AdminService = Depends(get_service),
) -> AdminBase:
    return await service.get_admin_by_id(db, admin_id)


@router.post(
    "/admin/",
    status_code=status.HTTP_201_CREATED,
    response_model=AdminBase,
    summary="Create new admin",
)
async def create_admin(
    admin: AdminCreateBase,
    db: AsyncSession = Depends(get_db),
    service: AdminService = Depends(get_service),
) -> AdminBase:
    return await service.create_admin(db, admin)


@router.put(
    "/admin/{admin_id}",
    status_code=status.HTTP_200_OK,
    response_model=AdminBase,
    summary="Update admin by id",
)
async def update_admin(
    admin_id: int,
    admin: AdminBase,
    db: AsyncSession = Depends(get_db),
    service: AdminService = Depends(get_service),
) -> AdminBase:
    return await service.update_admin(db, admin_id, admin)


@router.put(
    "/admin/products/active",
    status_code=status.HTTP_200_OK,
    response_model=ProductBase,
    summary="Update product active status",
)
async def update_product_active_status(
    product_id: int,
    admin_id: int,
    active: bool,
    db: AsyncSession = Depends(get_db),
    service: AdminService = Depends(get_service),
    manage_repository: ManageRepository = Depends(ManageRepository),
) -> ProductBase:
    return await service.update_product_active_status(
        db, product_id, active, admin_id, manage_repository
    )


@router.put(
    "/admin/user/active_state",
    status_code=status.HTTP_200_OK,
    response_model=UserBase,
    summary="Update user active state",
)
async def update_user_active_status(
    user_id: int,
    admin_id: int,
    active: bool,
    db: AsyncSession = Depends(get_db),
    service: AdminService = Depends(get_service),
    customer_repository: CustomersRepository = Depends(CustomersRepository),
    operate_repository: OperateRepository = Depends(OperateRepository),
) -> UserBase:
    return await service.update_casual_active_status(
        db, user_id, active, admin_id, customer_repository, operate_repository
    )


@router.put(
    "/admin/producers/active_state",
    status_code=status.HTTP_200_OK,
    response_model=UserBase,
    summary="Update producer active state",
)
async def update_producer_active_status(
    id_producers: int,
    admin_id: int,
    active: bool,
    db: AsyncSession = Depends(get_db),
    service: AdminService = Depends(get_service),
    carry_on_repository: CarryOnRepository = Depends(CarryOnRepository),
    producer_repository: ProducersRepository = Depends(ProducersRepository),
) -> UserBase:
    return await service.update_producer_active_status(
        db, id_producers, active, admin_id, carry_on_repository, producer_repository
    )


@router.post(
    "/admin/recipes",
    status_code=status.HTTP_201_CREATED,
    response_model=RecipesBase,
    summary="Create a new recipe from admin",
)
async def create_recipes_from_admin(
    admin_id: int,
    recipes: RecipesBase,
    db: AsyncSession = Depends(get_db),
    service: AdminService = Depends(get_service),
    recipes_repository: RecipesRepository = Depends(RecipesRepository),
    redac_repository: RedactRepository = Depends(RedactRepository),
) -> RecipesBase:
    return await service.create_recipes_from_admin(
        db, admin_id, recipes, recipes_repository, redac_repository
    )


@router.put(
    "/admin/{id_recipes}/modify_recipes",
    status_code=status.HTTP_200_OK,
    response_model=RecipesBase,
    summary="Modify a recipe from admin",
)
async def update_recipes_from_admin(
    admin_id: int,
    id_recipes: int,
    recipes: RecipesBase,
    db: AsyncSession = Depends(get_db),
    service: AdminService = Depends(get_service),
    recipes_repository: RecipesRepository = Depends(RecipesRepository),
    redac_repository: RedactRepository = Depends(RedactRepository),
) -> RecipesBase:
    return await service.update_recipes_from_admin(
        db, admin_id, id_recipes, recipes, recipes_repository, redac_repository
    )
