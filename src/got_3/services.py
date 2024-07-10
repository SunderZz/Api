from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from .repository import GotRepository
from .schema import GotBase
from common import model_to_dict


async def get_gots_service(
    got_repository: GotRepository, db: AsyncSession
) -> list[GotBase]:
    gots = await got_repository.get_got(db)
    gots_list = [model_to_dict(got) for got in gots]
    return [GotBase(**got_dict) for got_dict in gots_list]


async def get_got_by_id_service(
    got_id: int, got_repository: GotRepository, db: AsyncSession
) -> GotBase | list[GotBase]:
    got = await got_repository.get_got_by_id(db, got_id)
    if got is None:
        raise HTTPException(status_code=404, detail="got not found")
    if isinstance(got, list):
        gots_list = [model_to_dict(gots) for gots in got]
        return [GotBase(**got_dict) for got_dict in gots_list]
    return GotBase(**model_to_dict(got))


async def create_got_service(
    got: GotBase, got_repository: GotRepository, db: AsyncSession
) -> GotBase:
    id_code = got.Id_Code_Postal
    existing_code_postal = await got_repository.get_got_by_id(db, id_code)
    if existing_code_postal:
        return GotBase(**model_to_dict(existing_code_postal))
    new_got = await got_repository.create_got(db, got)
    return GotBase(**model_to_dict(new_got))


async def update_got_service(
    got: GotBase, got_id: int, got_repository: GotRepository, db: AsyncSession
) -> GotBase:
    updated_got = await got_repository.update_got(db, got, got_id)
    if updated_got is None:
        raise HTTPException(status_code=404, detail="got not found")
    return GotBase(**model_to_dict(updated_got))
