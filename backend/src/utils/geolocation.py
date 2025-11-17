import requests
import sys
from exception.exception import CustomException

class GeoLocationService:
    def get_location(self, text):
        try:
            url = "https://nominatim.openstreetmap.org/search"
            params = {"q": text, "format": "json", "limit": 1}

            res = requests.get(url, params=params, headers={"User-Agent": "hazard-app"}).json()

            if not res:
                return False, None, None

            country = res[0]["address"].get("country", "").lower()
            return country == "india", res[0]["lat"], res[0]["lon"]

        except Exception as e:
            raise CustomException(e, sys)

location_service = GeoLocationService()
