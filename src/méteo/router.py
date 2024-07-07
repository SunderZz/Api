from fastapi import APIRouter
from .services import scrape_weather


router = APIRouter(tags=["weather"])


@router.get("/weather")
async def get_weather():
    weather_data = scrape_weather()
    return weather_data
