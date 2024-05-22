from datetime import datetime
from fastapi import HTTPException
import users_adresses.models as models
import main as get_db
import requests
import json
from typing import Annotated, Optional
from .schema import UsersAdressesBase
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import engine, SessionLocal
from .repository import UsersAdressesRepository
from common import model_to_dict, url

from located.router import create_located,update_located,get_located_by_ids
from located.schema import LocatedBase
from located.repository import LocatedRepository
from code_postal.router import create_code_postales,update_code_postal,get_code_postal_value
from code_postal.schema import CodePostalBase, CodePostalIdBase
from code_postal.repository import CodePostalRepository
from city.router import create_city,update_city,get_city_by_names
from city.schema import CityBase, CityIdBase
from city.repository import CityRepository
from got_3.router import create_got,update_got,get_got_by_id
from got_3.schema import GotBase
from got_3.repository import GotRepository
from asso_33.router import create_asso_33
from asso_33.schema import Asso_33Base
from asso_33.repository import Asso_33Repository
from preference_ship.router import create_preference_ship
from preference_ship.schema import PreferenceshipBase
from preference_ship.repository import PreferenceshipRepository

def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close_all()

router = APIRouter(tags=["users_adresses"])

models.Base.metadata.create_all(bind=engine)

db_dependency= Annotated[Session, Depends(get_db)]


@router.get("/users/{adresse_id}/addresses", response_model=list[UsersAdressesBase])
async def get_user_addresses(adresse_id: int,user_adresse_repository: UsersAdressesRepository = Depends(UsersAdressesRepository), db: Session = Depends(get_db))->list[UsersAdressesBase]:
    adresses = await user_adresse_repository.get_user_addresses(db, adresse_id)
    if not adresses:
        raise HTTPException(status_code=404, detail="addresses not found")
    addresses_dict = [model_to_dict(adresse) for adresse in adresses]
    return [UsersAdressesBase(**adresse_dict) for adresse_dict in addresses_dict]

@router.get("/authorize_position/")
async def get_user_position(authorize: bool):
    if authorize:
        url_key = url
        geo_req = requests.get(url_key)
        geo_json = json.loads(geo_req.text)
    return geo_json


@router.post("/users_adresses/addresses", response_model=UsersAdressesBase)
async def create_user_an_address(authorize : bool,address: UsersAdressesBase,code_postal:CodePostalBase,city: CityBase,got_repository:GotRepository = Depends(GotRepository),asso_33_repository:Asso_33Repository = Depends(Asso_33Repository),preference_ship_repository:PreferenceshipRepository = Depends(PreferenceshipRepository),city_repositoy:CityRepository = Depends(CityRepository),code_postal_repository:CodePostalRepository= Depends(CodePostalRepository),located_repository:LocatedRepository= Depends(LocatedRepository),user_adresse_repository: UsersAdressesRepository = Depends(UsersAdressesRepository), db: Session = Depends(get_db)) -> UsersAdressesBase:
    acces = await get_user_position(authorize)
    Timestamp = datetime.now().isoformat()
    given_date_exact = datetime.strptime(Timestamp, "%Y-%m-%dT%H:%M:%S.%f").date()
    if acces:
        address_Latitude = acces['latitude']
        address_Longitude = acces['longitude']
        db_address = await user_adresse_repository.create_user_address(db, UsersAdressesBase(Adresse=address.Adresse,Phone=address.Phone,Creation=given_date_exact,Latitude=address_Latitude,Longitude=address_Longitude))
    else:
        db_address = await user_adresse_repository.create_user_address(db, UsersAdressesBase(Adresse=address.Adresse,Phone=address.Phone,Creation=given_date_exact))
    code =await create_code_postales(code_postal,code_postal_repository,db)
    value = await get_code_postal_value(code.code_postal,code_postal_repository,db)
    city_value = await create_city(city,city_repositoy,db)
    city_id = await get_city_by_names(city_value.Name,city_repositoy,db)
    await create_got(GotBase(Id_Code_Postal=value.Id_Code_Postal,Id_City=city_id.Id_City),got_repository,db)
    await create_located(LocatedBase(Id_Code_Postal=value.Id_Code_Postal,Id_Users_adresses=db_address.Id_Users_adresses),located_repository,db)
    ship_id = await create_preference_ship(PreferenceshipBase(),preference_ship_repository,db)
    await create_asso_33(Asso_33Base(Id_Preferenceship=ship_id.Id_Preferenceship,Id_Users_adresses=db_address.Id_Users_adresses),asso_33_repository,db)
    address_dict = model_to_dict(db_address) 
    return UsersAdressesBase(**address_dict)


@router.put("/users/{user_id}/addresses/{address_id}", response_model=UsersAdressesBase)
async def update_user_address(authorize:bool,address_id: int,address: UsersAdressesBase,postal_code: Optional[int] = None,city: Optional[str] = None,got_repository:GotRepository = Depends(GotRepository),city_repository:CityRepository = Depends(CityRepository),code_postal_repository:CodePostalRepository= Depends(CodePostalRepository),user_adresse_repository: UsersAdressesRepository = Depends(UsersAdressesRepository),located_repository:LocatedRepository= Depends(LocatedRepository), db: Session = Depends(get_db)) -> UsersAdressesBase:
    acces = await get_user_position(authorize)
    Timestamp = datetime.now().isoformat()
    given_date_exact = datetime.strptime(Timestamp, "%Y-%m-%dT%H:%M:%S.%f").date()
    if acces:
        address_Latitude = acces['latitude']
        address_Longitude = acces['longitude']
        updated_address = await user_adresse_repository.update_user_address(db, address_id, UsersAdressesBase(Adresse=address.Adresse,Phone=address.Phone,Modification=given_date_exact,Latitude=address_Latitude,Longitude=address_Longitude))
    else:
        updated_address = await user_adresse_repository.update_user_address(db,address_id, UsersAdressesBase(Adresse=address.Adresse,Phone=address.Phone,Modification=given_date_exact))
    if postal_code:
        code =await create_code_postales(CodePostalBase(code_postal=postal_code),code_postal_repository,db)
        value = await get_code_postal_value(code.code_postal,code_postal_repository,db)
        await create_located(LocatedBase(Id_Code_Postal=value.Id_Code_Postal,Id_Users_adresses=updated_address.Id_Users_adresses),located_repository,db)
    if city:
        city_value = await create_city(CityBase(Name=city),city_repository,db)
        value_city = await get_city_by_names(city_value.Name,city_repository,db)
        if city and postal_code:
            code =await create_code_postales(CodePostalBase(code_postal=postal_code),code_postal_repository,db)
            value = await get_code_postal_value(code.code_postal,code_postal_repository,db)
            print(value.Id_Code_Postal)
            print(value_city.Id_City)
            await update_got(GotBase(Id_City=value_city.Id_City,Id_Code_Postal=value.Id_Code_Postal),value.Id_Code_Postal,got_repository,db)
    address_dict = model_to_dict(updated_address)
    return UsersAdressesBase(**address_dict)
