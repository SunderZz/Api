from datetime import datetime
from fastapi import HTTPException
import users_adresses.models as models
from database import get_db
import requests
import json
from typing import Annotated, Optional
from .schema import UsersAdressesBase, UsersAdressesModifyBase, UsersCreateAdressesBase
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import engine2, AsyncSessionLocal
from .repository import UsersAdressesRepository
from common import model_to_dict
from fastapi import Form
from users_adresses.services import get_user_position

from located.router import create_located, update_located, get_located_by_ids
from located.schema import LocatedBase
from located.repository import LocatedRepository
from code_postal.router import (
    create_code_postales,
    update_code_postal,
    get_code_postal_value,
)
from code_postal.schema import CodePostalBase, CodePostalIdBase
from code_postal.repository import CodePostalRepository
from city.router import create_city, update_city, get_city_by_names
from city.schema import CityBase, CityIdBase
from city.repository import CityRepository
from got_3.router import create_got, update_got, get_got_by_id
from got_3.schema import GotBase
from got_3.repository import GotRepository
from asso_33.router import create_asso_33
from asso_33.schema import Asso_33Base
from asso_33.repository import Asso_33Repository
from preference_ship.router import create_preference_ship
from preference_ship.schema import PreferenceshipBase
from preference_ship.repository import PreferenceshipRepository

router = APIRouter(tags=["users_adresses"])


@router.get("/users/{adresse_id}/addresses", response_model=list[UsersAdressesBase])
async def get_user_addresses(
    adresse_id: int,
    user_adresse_repository: UsersAdressesRepository = Depends(UsersAdressesRepository),
    db: AsyncSession = Depends(get_db),
) -> list[UsersAdressesBase]:
    adresses = await user_adresse_repository.get_user_addresses(db, adresse_id)
    if not adresses:
        raise HTTPException(status_code=404, detail="addresses not found")
    addresses_dict = [model_to_dict(adresse) for adresse in adresses]
    return [UsersAdressesBase(**adresse_dict) for adresse_dict in addresses_dict]


@router.post("/users_adresses", response_model=UsersCreateAdressesBase)
async def create_user_an_address(
    Adresse: str = Form(...),
    Phone: str = Form(...),
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
    authorize: bool | None = None,
    db: AsyncSession = Depends(get_db),
) -> UsersCreateAdressesBase:
    acces = await get_user_position(authorize)
    Timestamp = datetime.now().isoformat()
    given_date_exact = datetime.strptime(Timestamp, "%Y-%m-%dT%H:%M:%S.%f").date()

    if acces:
        address_Latitude = acces["latitude"]
        address_Longitude = acces["longitude"]
        db_address = await user_adresse_repository.create_user_address(
            db,
            UsersAdressesBase(
                Adresse=Adresse,
                Phone=Phone,
                Creation=given_date_exact,
                Latitude=address_Latitude,
                Longitude=address_Longitude,
            ),
        )
    else:
        db_address = await user_adresse_repository.create_user_address(
            db,
            UsersAdressesBase(Adresse=Adresse, Phone=Phone, Creation=given_date_exact),
        )

    address_dict = model_to_dict(db_address)
    _address = UsersCreateAdressesBase(**address_dict)

    code = await create_code_postales(
        CodePostalBase(code_postal=code_postal), code_postal_repository, db
    )
    city_value = await create_city(CityBase(Name=city), city_repository, db)

    await create_got(
        GotBase(Id_Code_Postal=code.Id_Code_Postal, Id_City=city_value.Id_City),
        got_repository,
        db,
    )
    await create_located(
        LocatedBase(
            Id_Code_Postal=code.Id_Code_Postal,
            Id_Users_adresses=_address.Id_Users_adresses,
        ),
        located_repository,
        db,
    )

    ship_id = await create_preference_ship(
        PreferenceshipBase(), preference_ship_repository, db
    )
    await create_asso_33(
        Asso_33Base(
            Id_Preferenceship=ship_id.Id_Preferenceship,
            Id_Users_adresses=_address.Id_Users_adresses,
        ),
        asso_33_repository,
        db,
    )

    return _address


@router.put("/users_adresses/{address_id}", response_model=UsersAdressesModifyBase)
async def update_user_address(
    address_id: int,
    Adresse: str = Form(...),
    Phone: str = Form(...),
    code_postal: str = Form(...),
    city: str = Form(...),
    got_repository: GotRepository = Depends(GotRepository),
    city_repository: CityRepository = Depends(CityRepository),
    code_postal_repository: CodePostalRepository = Depends(CodePostalRepository),
    located_repository: LocatedRepository = Depends(LocatedRepository),
    user_adresse_repository: UsersAdressesRepository = Depends(UsersAdressesRepository),
    db: AsyncSession = Depends(get_db),
) -> UsersAdressesModifyBase:
    Timestamp = datetime.now().isoformat()
    given_date_exact = datetime.strptime(Timestamp, "%Y-%m-%dT%H:%M:%S.%f").date()
    address_data = UsersAdressesModifyBase(
        Adresse=Adresse, Phone=Phone, Modification=given_date_exact
    )
    db_address = await user_adresse_repository.update_user_address(
        db, address_id, address_data
    )

    if db_address is None:
        raise HTTPException(status_code=404, detail="Address not found")

    address_dict = model_to_dict(db_address)
    _address = UsersCreateAdressesBase(**address_dict)
    code_postal_data = CodePostalBase(code_postal=code_postal)
    city_data = CityBase(Name=city)
    code = await create_code_postales(code_postal_data, code_postal_repository, db)
    city_value = await create_city(city_data, city_repository, db)
    await create_got(
        GotBase(Id_Code_Postal=code.Id_Code_Postal, Id_City=city_value.Id_City),
        got_repository,
        db,
    )
    await create_located(
        LocatedBase(
            Id_Code_Postal=code.Id_Code_Postal,
            Id_Users_adresses=_address.Id_Users_adresses,
        ),
        located_repository,
        db,
    )
    return _address
