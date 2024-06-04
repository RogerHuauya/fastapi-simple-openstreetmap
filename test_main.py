import pytest

from fastapi.testclient import TestClient
from main import app


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
        assert float(response.json()[0]["lat"]) == pytest.approx(-12.0621065,
                                                                 0.1)
        assert float(response.json()[0]["lon"]) == pytest.approx(-77.0365256,
                                                                 0.1)


@pytest.mark.parametrize("city_name, expected_lat, expected_lon", [
    ("London", 51.5074, -0.1278),
    ("New York", 40.7128, -74.0060),
    ("Paris", 48.8566, 2.3522),
    ("Tokyo", 35.6895, 139.6917)
])
def test_the_result_is_correct_for_all_inputs(city_name: str,
                                              expected_lat: float,
                                              expected_lon: float):
    with TestClient(app) as client:
        response = client.get("/coordinates",
                              params={"city_name": city_name})
        assert float(response.json()[0]["lat"]) == pytest.approx(expected_lat,
                                                                 0.1)
        assert float(response.json()[0]["lon"]) == pytest.approx(expected_lon,
                                                                 0.1)
