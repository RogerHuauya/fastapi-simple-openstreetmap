import json

from fastapi.testclient import TestClient
from main import app

LIMA_PERU_COORDINATES = [
    {
        "place_id": 35725276,
        "licence": "Data © OpenStreetMap contributors, ODbL 1.0. http://osm.org/copyright",
        "osm_type": "relation",
        "osm_id": 12933390,
        "lat": "-12.0621065",
        "lon": "-77.0365256",
        "class": "boundary",
        "type": "administrative",
        "place_rank": 10,
        "importance": 0.673001488378204,
        "addresstype": "city",
        "name": "Lima Metropolitan Area",
        "display_name": "Lima Metropolitan Area, Lima, Peru",
        "boundingbox": [
            "-12.5199316",
            "-11.5724356",
            "-77.1992129",
            "-76.6208244"
        ]
    },
    {
        "place_id": 35510272,
        "licence": "Data © OpenStreetMap contributors, ODbL 1.0. http://osm.org/copyright",
        "osm_type": "relation",
        "osm_id": 1944659,
        "lat": "-12.2001093",
        "lon": "-76.2850579",
        "class": "boundary",
        "type": "administrative",
        "place_rank": 8,
        "importance": 0.501976120195012,
        "addresstype": "state",
        "name": "Lima",
        "display_name": "Lima, Peru",
        "boundingbox": [
            "-13.3241714",
            "-10.2741856",
            "-77.8863105",
            "-75.5075000"
        ]
    },
    {
        "place_id": 37971044,
        "licence": "Data © OpenStreetMap contributors, ODbL 1.0. http://osm.org/copyright",
        "osm_type": "relation",
        "osm_id": 1944670,
        "lat": "-12.0002116",
        "lon": "-76.8330796",
        "class": "boundary",
        "type": "administrative",
        "place_rank": 12,
        "importance": 0.483483532074075,
        "addresstype": "region",
        "name": "Province of Lima",
        "display_name": "Province of Lima, Lima Metropolitan Area, Lima, Peru",
        "boundingbox": [
            "-12.5199316",
            "-11.5724356",
            "-77.1992129",
            "-76.6208244"
        ]
    }
]


def test_can_call_existent_endpoints_of_the_api():
    with TestClient(app) as client:
        response = client.get("/distance",
                              params={"lat1": 1, "lon1": 1, "lat2": 2,
                                      "lon2": 2})
        assert response.status_code == 200

        response = client.get("/coordinates",
                              params={"city_name": "lima,peru"})
        assert response.status_code == 200


def test_can_call_nonexistent_endpoints_of_the_api():
    with TestClient(app) as client:
        response = client.get("/nonexistent")
        assert response.status_code == 404


def test_endpoint_returns_something():
    with TestClient(app) as client:
        response = client.get("/distance",
                              params={"lat1": 1, "lon1": 1, "lat2": 2,
                                      "lon2": 2})
        assert response.json() != {}

        response = client.get("/coordinates",
                              params={"city_name": "lima,peru"})
        assert response.json() != {}


def test_the_result_is_correct_for_simple_cases():
    with TestClient(app) as client:
        response = client.get("/coordinates",
                              params={"city_name": "lima,peru"})
        lat = LIMA_PERU_COORDINATES[0]["lat"]
        lon = LIMA_PERU_COORDINATES[0]["lon"]
        assert response.json()[0]["lat"] == lat
        assert response.json()[0]["lon"] == lon
