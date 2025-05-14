import pytest
import requests

def test_dog_main_page(base_url):
    res = requests.get(f"{base_url}")
    assert res.status_code == 200

def test_random_image():
    response = requests.get("https://dog.ceo/api/breeds/image/random")
    assert response.status_code == 200
    assert response.json().get("status") == "success"

def test_breeds_list():
    response = requests.get("https://dog.ceo/api/breeds/list/all")
    assert response.status_code == 200
    data = response.json()
    assert data.get("status") == "success"
    assert data.get("message")
    breeds = data.get("message")
    assert isinstance(breeds, dict)
    for breed, subbreeds in breeds.items():
        assert isinstance(breed, str)
        assert isinstance(subbreeds, list)
        for sub in subbreeds:
            assert isinstance(sub, str)

@pytest.mark.parametrize("breed", [
    "akita",
    "havanese",
    "dingo"
])
def test_one_breed(breed):
    response = requests.get(f"https://dog.ceo/api/breed/{breed}/images/random")
    assert response.status_code == 200
    data = response.json()
    assert data.get("message") is not None
    assert data.get("status") == "success"

@pytest.mark.parametrize("breed", [
    "hound",
    "boxer",
    "chihuahua"
])
def test_images(breed):
    response = requests.get(f"https://dog.ceo/api/breed/{breed}/images")
    assert response.status_code == 200
    data = response.json()
    images = data.get("message")
    assert isinstance(images, list)
    assert len(images) > 0
    for img_url in images:
        assert isinstance(img_url, str)
        assert img_url.startswith(f"https://images.dog.ceo/breeds/{breed}")
        assert len(img_url) > len("https://images.dog.ceo/breeds")
    assert data.get("status") == "success"