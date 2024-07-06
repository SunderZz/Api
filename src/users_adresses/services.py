import requests
import json
from typing import Optional
from fastapi import HTTPException

from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from users_adresses.schema import UsersAdressesBase, UsersCreateAdressesBase, UsersAdressesModifyBase
from users_adresses.repository import UsersAdressesRepository
from common import model_to_dict
from code_postal.schema import CodePostalBase
from city.schema import CityBase
from got_3.schema import GotBase
from located.schema import LocatedBase
from asso_33.schema import Asso_33Base
from preference_ship.schema import PreferenceshipBase
from code_postal.repository import CodePostalRepository
from city.repository import CityRepository
from got_3.repository import GotRepository
from located.repository import LocatedRepository
from asso_33.repository import Asso_33Repository
from preference_ship.repository import PreferenceshipRepository

from located.router import create_located
from located.schema import LocatedBase
from located.repository import LocatedRepository
from code_postal.router import (
    create_code_postales
)
from code_postal.schema import CodePostalBase
from code_postal.repository import CodePostalRepository
from city.router import create_city
from city.schema import CityBase
from city.repository import CityRepository
from got_3.router import create_got
from got_3.schema import GotBase
from got_3.repository import GotRepository
from asso_33.router import create_asso_33
from asso_33.schema import Asso_33Base
from asso_33.repository import Asso_33Repository
from preference_ship.router import create_preference_ship
from preference_ship.schema import PreferenceshipBase
from preference_ship.repository import PreferenceshipRepository

url = "http://api.ipstack.com/check?access_key=e6b90ef1b887acd19f5921c37c45c00e"


# Retrieve user position with authorisation
async def get_user_position(authorize: bool):
    if authorize:
        url_key = url
        geo_req = requests.get(url_key)
        geo_json = json.loads(geo_req.text)
        return geo_json
    return None

#create user adresse
async def create_user_address_service(
    Adresse: str,
    Phone: str,
    code_postal: str,
    city: str,
    acces: Optional[dict],
    given_date: datetime,
    user_adresse_repository: UsersAdressesRepository,
    code_postal_repository: CodePostalRepository,
    city_repository: CityRepository,
    got_repository: GotRepository,
    located_repository: LocatedRepository,
    asso_33_repository: Asso_33Repository,
    preference_ship_repository: PreferenceshipRepository,
    db: AsyncSession,
) -> UsersCreateAdressesBase:
    if acces:
        address_Latitude = acces["latitude"]
        address_Longitude = acces["longitude"]
        db_address = await user_adresse_repository.create_user_address(
            db,
            UsersAdressesBase(
                Adresse=Adresse,
                Phone=Phone,
                Creation=given_date,
                Latitude=address_Latitude,
                Longitude=address_Longitude,
            ),
        )
    else:
        db_address = await user_adresse_repository.create_user_address(
            db,
            UsersAdressesBase(Adresse=Adresse, Phone=Phone, Creation=given_date),
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

async def update_user_address_service(
    address_id: int,
    Adresse: str,
    Phone: str,
    code_postal: str,
    city: str,
    given_date: datetime,
    user_adresse_repository: UsersAdressesRepository,
    code_postal_repository: CodePostalRepository,
    city_repository: CityRepository,
    got_repository: GotRepository,
    located_repository: LocatedRepository,
    db: AsyncSession,
) -> UsersAdressesModifyBase:
    address_data = UsersAdressesModifyBase(
        Adresse=Adresse, Phone=Phone, Modification=given_date
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
