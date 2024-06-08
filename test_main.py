import pytest

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_can_call_existent_endpoints_of_the_api():
    response = client.get(
        "/distance", params={"lat1": 1, "lon1": 1, "lat2": 2, "lon2": 2}
    )
    assert response.status_code == 200

    response = client.get("/coordinates", params={"city_name": "lima,peru"})
    assert response.status_code == 200


def test_can_call_nonexistent_endpoints_of_the_api():
    response = client.get("/nonexistent")
    assert response.status_code == 404


def test_endpoint_with_incorrect_number_of_parameters():
    response = client.get("/distance", params={"lat1": 1, "lon1": 1, "lat2": 2})
    assert response.status_code == 422  # Missing required parameter

    response = client.get("/coordinates", params={})
    assert response.status_code == 422  # Missing required parameter


def test_endpoint_returns_something():
    response = client.get(
        "/distance", params={"lat1": 1, "lon1": 1, "lat2": 2, "lon2": 2}
    )
    assert response.json() != {}

    response = client.get("/coordinates", params={"city_name": "lima,peru"})
    assert response.json() != {}


def test_the_result_is_correct_for_simple_cases():
    response = client.get("/coordinates", params={"city_name": "lima,peru"})
    assert float(response.json()[0]["lat"]) == pytest.approx(-12.0621065, 0.1)
    assert float(response.json()[0]["lon"]) == pytest.approx(-77.0365256, 0.1)


@pytest.mark.parametrize(
    "city_name, expected_lat, expected_lon",
    [
        ("London", 51.5074, -0.1278),
        ("New York", 40.7128, -74.0060),
        ("Paris", 48.8566, 2.3522),
        ("Tokyo", 35.6895, 139.6917),
        ("Sydney", -33.8688, 151.2093),
        ("Lima", -12.0464, -77.0428),
        ("Madrid", 40.4168, -3.7038),
        ("Berlin", 52.5200, 13.4050),
        ("Rome", 41.9028, 12.4964),
        ("Buenos Aires", -34.6037, -58.3816),
        ("Mexico City", 19.4326, -99.1332),
        ("Beijing", 39.9042, 116.4074),
        ("Seoul", 37.5665, 126.9780),
        ("Cape Town", -33.9249, 18.4241),
        ("Nairobi", -1.2921, 36.8219),
        ("Bogota", 4.7109, -74.0721),
        ("Santiago de Chile", -33.4489, -70.6693),
        ("Lisbon", 38.7223, -9.1393),
        ("Istanbul", 41.0082, 28.9784),
        ("Kiev", 50.4501, 30.5234),
        ("Bangalore", 12.9716, 77.5946),
        ("Melbourne", -37.8136, 144.9631),
        ("Auckland", -36.8485, 174.7633),
        ("Vancouver", 49.2827, -123.1207),
        ("Los Angeles", 34.0522, -118.2437),
        ("Chicago", 41.8781, -87.6298),
        ("Houston", 29.7604, -95.3698),
        ("Miami", 25.7617, -80.1918),
        ("Toronto", 43.6511, -79.3470),
        ("Montreal", 45.5017, -73.5673),
    ],
)
def test_the_result_is_correct_for_all_inputs(
    city_name: str, expected_lat: float, expected_lon: float
):
    response = client.get("/coordinates", params={"city_name": city_name})
    assert float(response.json()[0]["lat"]) == pytest.approx(expected_lat, 0.2)
    assert float(response.json()[0]["lon"]) == pytest.approx(expected_lon, 0.2)
