from fastapi import HTTPException, APIRouter, Depends, Form
from sqlalchemy.ext.asyncio import AsyncSession

from users_adresses.schema import (
    UsersAdressesBase,
    UsersAdressesModifyBase,
    UsersCreateAdressesBase,
)
from users_adresses.repository import UsersAdressesRepository
from database import get_db
from common import get_actual_ts
from users_adresses.services import (
    create_user_address_service,
    update_user_address_service,
)
from users_adresses.services import get_user_position

from located.repository import LocatedRepository

from code_postal.repository import CodePostalRepository
from city.repository import CityRepository
from got_3.repository import GotRepository
from asso_33.repository import Asso_33Repository
from preference_ship.repository import PreferenceshipRepository

router = APIRouter(tags=["users_adresses"])


@router.get(
    "/users_adresses/{adresse_id}",
    response_model=list[UsersAdressesBase] | UsersAdressesBase,
    description="retrieve adresse of an user",
)
async def get_user_addresse(
    adresse_id: int,
    user_adresse_repository: UsersAdressesRepository = Depends(UsersAdressesRepository),
    db: AsyncSession = Depends(get_db),
) -> list[UsersAdressesBase] | UsersAdressesBase:
    adresses = await user_adresse_repository.get_user_addresses(db, adresse_id)
    if not adresses:
        raise HTTPException(status_code=404, detail="addresses not found")
    return adresses


@router.post(
    "/users_adresses",
    response_model=UsersCreateAdressesBase,
    description="create an adresse of an user",
)
async def create_user_an_address(
    Adresse: str = Form(...),
    Phone: int = Form(...),
    code_postal: str = Form(...),
    city: str = Form(...),
    got_repository: GotRepository = Depends(GotRepository),
    asso_33_repository: Asso_33Repository = Depends(Asso_33Repository),
    preference_ship_repository: PreferenceshipRepository = Depends(
        PreferenceshipRepository
    ),
    city_repository: CityRepository = Depends(CityRepository),
    code_postal_repository: CodePostalRepository = Depends(CodePostalRepository),
    located_repository: LocatedRepository = Depends(LocatedRepository),
    user_adresse_repository: UsersAdressesRepository = Depends(UsersAdressesRepository),
    authorize: bool = bool,
    db: AsyncSession = Depends(get_db),
) -> UsersCreateAdressesBase:
    acces = await get_user_position(authorize)
    given_date = get_actual_ts()
    return await create_user_address_service(
        Adresse,
        Phone,
        code_postal,
        city,
        acces,
        given_date,
        user_adresse_repository,
        code_postal_repository,
        city_repository,
        got_repository,
        located_repository,
        asso_33_repository,
        preference_ship_repository,
        db,
    )


@router.put(
    "/users_adresses/{address_id}",
    response_model=UsersAdressesModifyBase,
    description="update an adresse of an user",
)
async def update_user_address(
    address_id: int,
    Adresse: str = Form(...),
    Phone: int = Form(...),
    code_postal: str = Form(...),
    city: str = Form(...),
    got_repository: GotRepository = Depends(GotRepository),
    city_repository: CityRepository = Depends(CityRepository),
    code_postal_repository: CodePostalRepository = Depends(CodePostalRepository),
    located_repository: LocatedRepository = Depends(LocatedRepository),
    user_adresse_repository: UsersAdressesRepository = Depends(UsersAdressesRepository),
    db: AsyncSession = Depends(get_db),
) -> UsersAdressesModifyBase:
    given_date = get_actual_ts()
    return await update_user_address_service(
        address_id,
        Adresse,
        Phone,
        code_postal,
        city,
        given_date,
        user_adresse_repository,
        code_postal_repository,
        city_repository,
        got_repository,
        located_repository,
        db,
    )
