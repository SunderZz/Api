import requests
import json

url = "http://api.ipstack.com/check?access_key=e6b90ef1b887acd19f5921c37c45c00e"

# Retrieve user position with authorisation
async def get_user_position(authorize: bool):
    if authorize:
        url_key = url
        geo_req = requests.get(url_key)
        geo_json = json.loads(geo_req.text)
        return geo_json
    return None
