from sqlalchemy.ext.asyncio import AsyncSession
from .models import Product
from sqlalchemy.future import select


class ProductRepository:
    async def get_product(self, db: AsyncSession) -> list[Product]:
        result = await db.execute(select(Product))
        return result.scalars().all()

    async def get_product_query(self, db: AsyncSession, product: int) -> Product:
        result = await db.execute(select(Product).filter(Product.Id_Product == product))
        return result.scalar_one_or_none()

    async def get_product_id_by_name(
        self, db: AsyncSession, name: str
    ) -> list[Product]:
        result = await db.execute(select(Product).filter(Product.Name == name))
        return result.scalars().all()

    async def get_product_id(self, db: AsyncSession, id: int) -> Product:
        result = await db.execute(select(Product).filter(Product.Id_Product == id))
        return result.scalar_one_or_none()

    async def get_product_by_discount(self, db: AsyncSession) -> list[Product]:
        result = await db.execute(
            select(Product).filter(Product.Discount.isnot(None), Product.Discount > 0)
        )
        return result.scalars().all()

    async def get_products_by_name(
        self, db: AsyncSession, product_name: str
    ) -> Product | list[Product] | None:
        result = await db.execute(select(Product).filter(Product.Name == product_name))
        products = result.scalars().all()
        if not products:
            return None

        if len(products) == 1:
            return products[0]

        return products

    async def create_product(self, db: AsyncSession, product: Product) -> Product:
        db_product = Product(**product.dict())
        db.add(db_product)
        await db.commit()
        await db.refresh(db_product)
        return db_product

    async def update_product(
        self, db: AsyncSession, product: int, db_product_data: Product
    ) -> Product:
        result = await db.execute(select(Product).filter(Product.Id_Product == product))
        db_product = result.scalar_one_or_none()
        if db_product is None:
            return None
        for key, value in db_product_data.__dict__.items():
            if hasattr(db_product, key) and value is not None:
                setattr(db_product, key, value)
        await db.commit()
        return db_product
