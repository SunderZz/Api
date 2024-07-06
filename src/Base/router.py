import ipstack
import requests
import json
import users.models as models
from typing import Annotated
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from database import engine2, AsyncSessionLocal


router = APIRouter(tags=["health"])


send_url = "http://api.ipstack.com/check?access_key=e6b90ef1b887acd19f5921c37c45c00e"
geo_req = requests.get(send_url)
geo_json = json.loads(geo_req.text)
latitude = geo_json["latitude"]
longitude = geo_json["longitude"]
