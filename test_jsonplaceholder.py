import requests
import pytest

def test_jsonplaceholder(base_url):
    res = requests.get(f"{base_url}")
    assert res.status_code == 200
@pytest.mark.parametrize("title, body, userId, expected_status", [
    ("foo", "bar", 1, 201),
    ("", "bar", 1, 201), #ожидаем статус-код 201, потому что это фейковый ресурс. В реальности ожидали бы 400
    ("foo", "", 1, 201), #в реальности ожидали бы 400
    ("foo", "bar", None, 201), #в реальности ожидали бы 400
    ("test", "data", 99, 201)
])
def test_add_post(title, body, userId, expected_status):
    url = "https://jsonplaceholder.typicode.com/posts"
    payload = {
        "title": title,
        "body": body,
    }
    if userId is not None:
        payload["userId"] = userId

    headers = {
        "Content-type": "application/json; charset=UTF-8",
    }
    response = requests.post(url, json=payload, headers=headers)
    assert response.status_code == expected_status
    if response.status_code == 201:
        response_json = response.json()
        assert response_json["title"] == payload["title"]
        assert response_json["body"] == payload["body"]
        if "userId" in payload:
            assert response_json["userId"] == payload["userId"]

@pytest.mark.parametrize("id, title, body, expected_status", [
    (1, "sunt aut facere repellat provident occaecati excepturi optio reprehenderit", "bar", 200),
    (1, "", "bar", 200),
    (1, "foo", "", 200),
    (2, "test", "data", 200),
    (0, "foo", "bar", 500), #Ожидаем 500 из-за специфики апи, должно быть 404
    (None, "foo", "bar", 404)
])
def test_update_post(id, title, body, expected_status):
    if id is None:
        # Невозможно сформировать корректный URL
        url = "https://jsonplaceholder.typicode.com/posts/"
    else:
        url = f"https://jsonplaceholder.typicode.com/posts/{id}"

    payload = {
        "title": title,
        "body": body,
    }

    headers = {
        "Content-type": "application/json; charset=UTF-8",
    }
    response = requests.put(url, json=payload, headers=headers)
    assert response.status_code == expected_status
    if response.status_code == 200:
        response_json = response.json()
        assert response_json["title"] == payload["title"]
        assert response_json["body"] == payload["body"]

def test_patch_post():
    id = 1
    url = f"https://jsonplaceholder.typicode.com/posts/{id}"
    payload = {
        "title": "patched"
    }

    headers = {
        "Content-type": "application/json; charset=UTF-8",
    }
    response = requests.put(url, json=payload, headers=headers)
    assert response.status_code == 200
    if response.status_code == 200:
        response_json = response.json()
        assert response_json["title"] == payload["title"]

def test_delete_post():
    id = 1
    url = f"https://jsonplaceholder.typicode.com/posts/{id}"
    response = requests.delete(url)
    assert response.status_code == 200
    get_response = requests.get(url)
    assert get_response.status_code == 200  #В реальности ожидали бы 404