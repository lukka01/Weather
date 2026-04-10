import requests
import logging

logger = logging.getLogger(__name__)

OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"
DEFAULT_LATITUDE  = 41.6941
DEFAULT_LONGITUDE = 44.8337


def fetch_weather(latitude=DEFAULT_LATITUDE, longitude=DEFAULT_LONGITUDE):
    params = {
        "latitude":        latitude,
        "longitude":       longitude,
        "current_weather": True,
    }

    try:
        response = requests.get(OPEN_METEO_URL, params=params, timeout=10)
        response.raise_for_status()
    except requests.exceptions.ConnectionError:
        raise ConnectionError("გარე API-სთან კავშირი ვერ მოხდა.")
    except requests.exceptions.Timeout:
        raise ConnectionError("API მოთხოვნამ დრო გადააჭარბა.")
    except requests.exceptions.HTTPError as exc:
        raise ValueError(f"API HTTP შეცდომა: {response.status_code}") from exc

    try:
        current = response.json()["current_weather"]
        return {
            "latitude":     latitude,
            "longitude":    longitude,
            "temperature":  current["temperature"],
            "wind_speed":   current["windspeed"],
            "weather_code": current["weathercode"],
        }
    except KeyError as exc:
        raise ValueError("API-ს პასუხი მოულოდნელი ფორმატისაა.") from exc