from sqlalchemy.ext.asyncio import AsyncSession
from .schema import Asso_33Base
from .repository import Asso_33Repository
from common import model_to_dict
from fastapi import HTTPException
from .repository import Asso_33Repository


async def get_all_asso_33_services(
    asso_33_repository: Asso_33Repository, db: AsyncSession
) -> list[Asso_33Base]:
    asso_33s = await asso_33_repository.get_asso_33(db)
    return [Asso_33Base(**model_to_dict(asso_33)) for asso_33 in asso_33s]


async def get_asso_33_by_id_services(
    asso_33_repository: Asso_33Repository, db: AsyncSession, asso_33_id: int
) -> Asso_33Base:
    asso_33 = await asso_33_repository.get_asso_33_by_id(db, asso_33_id)
    if not asso_33:
        raise HTTPException(status_code=404, detail="asso_33 not found")
    return Asso_33Base(**model_to_dict(asso_33))


async def create_asso_33_services(
    asso_33_repository: Asso_33Repository, asso_33: Asso_33Base, db: AsyncSession
) -> Asso_33Base:
    new_asso_33 = await asso_33_repository.create_assos_33(db, asso_33)
    return Asso_33Base(**model_to_dict(new_asso_33))


async def update_asso_33_services(
    db: AsyncSession,
    asso_33_repository: Asso_33Repository,
    asso_33_id: int,
    asso_33: Asso_33Base,
) -> Asso_33Base:
    updated_asso_33 = await asso_33_repository.update_asso_33(db, asso_33_id, asso_33)
    if not updated_asso_33:
        raise HTTPException(status_code=404, detail="asso_33 not found")
    return Asso_33Base(**model_to_dict(updated_asso_33))
