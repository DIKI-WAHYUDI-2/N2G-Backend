import pytest

def get_auth_cookies(client):
    response = client.post('/auth/login', json={
        "username": "testadmin",
        "password": "testpassword"
    })
    return response.headers.getlist('Set-Cookie')

def test_analyze_valid_payload(client):
    cookies = get_auth_cookies(client)
    headers = {'Cookie': '; '.join(cookies)} if cookies else {}

    payload = {
        "title": "Prabowo menang pemilu",
        "content": "Menurut berita..."
    }
    resp = client.post('/news/analyze', json=payload, headers=headers)
    assert resp.status_code == 200
    data = resp.get_json()
    assert data['status'] == "success"
    assert data['sentiment'] in ["positif", "negatif", "netral"]

def test_analyze_missing_title(client):
    cookies = get_auth_cookies(client)
    headers = {'Cookie': '; '.join(cookies)} if cookies else {}

    resp = client.post('/news/analyze', json={"content": "test"}, headers=headers)
    assert resp.status_code == 400
    assert resp.get_json()['message'] == "title wajib diisi"

