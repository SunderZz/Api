from sqlalchemy.ext.asyncio import AsyncSession

from users.models import Users
from products.models import Product
from .models import Admin
from sqlalchemy.future import select


class AdminRepository:
    async def get_admin(self, db: AsyncSession) -> list[Admin]:
        result = await db.execute(select(Admin))
        return result.scalars().all()

    async def get_admin_query(self, db: AsyncSession, admin: int) -> Admin:
        result = await db.execute(select(Admin).filter(Admin.Id_Users == admin))
        return result.scalar_one_or_none()

    async def create_admin(self, db: AsyncSession, admin: Admin) -> Admin:
        db_admin = Admin(**admin.dict())
        db.add(db_admin)
        await db.commit()
        await db.refresh(db_admin)
        return db_admin

    async def update_admin(
        self, db: AsyncSession, admin: int, db_admin_data: Admin
    ) -> Admin:
        result = await db.execute(select(Admin).filter(Admin.Id_Admin == admin))
        db_admin = result.scalar_one_or_none()
        if db_admin is None:
            return None
        for key, value in db_admin_data.__dict__.items():
            if hasattr(db_admin, key) and value is not None:
                setattr(db_admin, key, value)
        await db.commit()
        return db_admin

    async def modify_user_active_status(
        self, db: AsyncSession, user_id: int, active: bool
    ) -> Users:
        result = await db.execute(select(Users).filter(Users.Id_Users == user_id))
        user = result.scalar_one_or_none()
        if user:
            user.active = active
            await db.commit()
            await db.refresh(user)
        return user

    async def update_product_active_status(
        self, db: AsyncSession, product_id: int, active: bool
    ) -> Product:
        result = await db.execute(
            select(Product).filter(Product.Id_Product == product_id)
        )
        product = result.scalar_one_or_none()
        if product:
            product.Active = active
            await db.commit()
            await db.refresh(product)
        return product
