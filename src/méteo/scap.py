import requests
from bs4 import BeautifulSoup


def scrape_weather():
    url = "https://meteo.francetvinfo.fr/previsions-meteo-outremer/la-reunion"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")

        forecast_items = soup.find("ul", {"id": "next-days-forecast-items"}).find_all(
            "li"
        )

        weather_data = []

        for item in forecast_items:
            city = item.find("span", class_="header").find_all("span")[0].text.strip()
            temps = item.find("span", class_="temperature").find_all("span")
            temp_max = temps[0].text.strip()
            temp_min = temps[1].text.strip()
            weather_data.append(
                {"city": city, "temp_max": temp_max, "temp_min": temp_min}
            )

        return weather_data
    else:
        print(f"Cannot retrieve data: {response.status_code}")
        return []
