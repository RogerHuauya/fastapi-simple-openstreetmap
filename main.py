from fastapi import FastAPI
from fastapi.responses import JSONResponse
import requests

app = FastAPI()

OPENSTREETMAP_URL = "https://nominatim.openstreetmap.org/search"


def fetch_from_openstreetmap(city_name: str):
    url = f"{OPENSTREETMAP_URL}?q={city_name}&format=json"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


@app.exception_handler(404)
async def not_found(request, exc):
    return JSONResponse(
        status_code=404,
        content={"detail": "Not Found"},
    )


@app.get("/distance/")
async def get_distance(lat1, lon1, lat2, lon2):
    return {"message": f"Working"}


@app.get("/coordinates")
async def get_coordinates(city_name: str):
    coordinates_json = fetch_from_openstreetmap(city_name)
    return coordinates_json
