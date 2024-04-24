import users.models as models
from typing import Annotated
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
import main as get_db
from database import engine, SessionLocal
import requests
import json

def get_db():
    db = SessionLocal
    try: 
        yield db
    finally:
        db.close_all()

router = APIRouter(tags=["health"])

models.Base.metadata.create_all(bind=engine)

db_dependency= Annotated[Session, Depends(get_db)]


@router.get("/", status_code= status.HTTP_201_CREATED)
async def health(db: db_dependency):
    response_data = requests.get('https://www.iplocation.net/go/ipinfo').text
    try:
        response_json_data = json.loads(response_data)
        location = response_json_data["loc"].split(",")
        print("Latitude: %s" % location[0])
        print("Longitude: %s" % location[1])
    except ValueError:
        print("Exception happened while loading data")




