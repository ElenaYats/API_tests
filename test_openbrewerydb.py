import pytest
import requests

def test_openbrewerydb(base_url):
    res = requests.get(f"{base_url}")
    assert res.status_code == 200

def test_random_brewery_structure():
    response = requests.get("https://api.openbrewerydb.org/v1/breweries/random")
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert isinstance(data[0], dict)

def test_required_fields():
    response = requests.get("https://api.openbrewerydb.org/v1/breweries/random")
    data = response.json()
    brewery = data[0]
    required_fields = [
        "id", "name", "brewery_type", "city", "state_province",
        "postal_code", "country", "longitude", "latitude", "phone", "state"
    ]
    for field in required_fields:
        assert field in brewery, f"Missing field: {field}"

@pytest.mark.parametrize("country", [
    "poland",
    "portugal",
    "south korea"
])
def test_search_brewery_in_country(country):
    response = requests.get(f"https://api.openbrewerydb.org/v1/breweries/?by_country={country}")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    for brewery in data:
        assert brewery.get("country", "").lower() == country.lower()
        
@pytest.mark.parametrize("city", [
    "san diego",
    "lewes",
    "brighton"
])
def test_search_brewery_in_country(city):
    response = requests.get(f"https://api.openbrewerydb.org/v1/breweries/?by_country={city}")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    for brewery in data:
        assert brewery.get("city", "").lower() == city.lower()