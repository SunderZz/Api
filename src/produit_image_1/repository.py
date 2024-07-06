from sqlalchemy.ext.asyncio import AsyncSession
from .models import Produit_Image
from sqlalchemy.future import select


class ProduitImageRepository:
    async def get_produit_image(self, db: AsyncSession) -> list[Produit_Image]:
        result = await db.execute(select(Produit_Image))
        return result.scalars().all()

    async def get_produit_image_query(
        self, db: AsyncSession, produit_image: int
    ) -> Produit_Image:
        result = await db.execute(
            select(Produit_Image).filter(
                Produit_Image.Id_Produit_Image == produit_image
            )
        )
        return result.scalar_one_or_none()

    async def create_produit_image(
        self, db: AsyncSession, produit_image: Produit_Image
    ) -> Produit_Image:
        db_produit_image = Produit_Image(**produit_image.dict())
        db.add(db_produit_image)
        await db.commit()
        await db.refresh(db_produit_image)
        return db_produit_image

    async def update_Produit_Image(
        self,
        db: AsyncSession,
        produit_image_id: int,
        db_produit_image_data: Produit_Image,
    ) -> Produit_Image:
        result = await db.execute(
            select(Produit_Image).filter(
                Produit_Image.Id_Produit_Image == produit_image_id
            )
        )
        db_produit_image = result.scalar_one_or_none()
        if db_produit_image is None:
            return None
        for key, value in db_produit_image_data.__dict__.items():
            if hasattr(db_produit_image, key) and value is not None:
                setattr(db_produit_image, key, value)
        await db.commit()
        return db_produit_image
