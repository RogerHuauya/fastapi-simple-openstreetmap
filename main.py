import requests

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from geopy.distance import geodesic

app = FastAPI()

OPENSTREETMAP_URL = "https://nominatim.openstreetmap.org/search"


def fetch_from_openstreetmap(city_name: str):
    """
    Fetch the coordinates of a city from OpenStreetMap.
    :param city_name: The name of the city.
    :return: The JSON response from OpenStreetMap.
    """
    url = f"{OPENSTREETMAP_URL}?q={city_name}&format=json"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/58.0.3029.110 Safari/537.3"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()


def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the distance between two points in kilometers.
    :param lat1: Latitude of the first point.
    :param lon1: Longitude of the first point.
    :param lat2: Latitude of the second point.
    :param lon2: Longitude of the second point.
    :return: The distance between the two points in kilometers.
    """
    return geodesic((lat1, lon1), (lat2, lon2)).kilometers


@app.exception_handler(404)
async def not_found(request, exc):
    return JSONResponse(
        status_code=404,
        content={"detail": "Not Found"},
    )


@app.get("/distance/")
async def get_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the distance between two points.
    :param lat1:
    :param lon1:
    :param lat2:
    :param lon2:
    :return:
    """
    distance = calculate_distance(lat1, lon1, lat2, lon2)
    return {"distance": distance}


@app.get("/coordinates")
async def get_coordinates(city_name: str):
    """
    Get the coordinates of a city.
    :param city_name:
    :return:
    """
    coordinates_json = fetch_from_openstreetmap(city_name)
    return coordinates_json
