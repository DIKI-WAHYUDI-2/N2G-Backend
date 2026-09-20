import pytest
import sys
from unittest.mock import patch

def get_auth_cookies(client):
    response = client.post('/auth/login', json={
        "username": "testadmin",
        "password": "testpassword"
    })
    return response.headers.getlist('Set-Cookie')

def test_scrape_news_invalid_payload(client):
    cookies = get_auth_cookies(client)
    headers = {'Cookie': '; '.join(cookies)} if cookies else {}

    # Empty payload
    resp = client.post('/scrape', json={}, headers=headers)
    assert resp.status_code == 400

    # Missing start_date
    resp = client.post('/scrape', json={"keyword": "Prabowo"}, headers=headers)
    assert resp.status_code == 400

    # Unknown field
    resp = client.post('/scrape', json={"keyword": "A", "start_date": "2026-09-01", "unknown": "X"}, headers=headers)
    assert resp.status_code == 400

@patch('apps.service.news_service.NewsService.scrape_classify_and_save')
def test_scrape_news_valid_payload(mock_scrape, client):
    # Mocking the pipeline to avoid actual web scraping during tests
    mock_scrape.return_value = {
        "count": 5,
        "saved_count": 5,
        "skipped_count": 0,
        "failed_count": 0,
        "data": [],
        "export_file": None
    }
    
    cookies = get_auth_cookies(client)
    headers = {'Cookie': '; '.join(cookies)} if cookies else {}

    resp = client.post('/scrape', json={
        "keyword": "Prabowo",
        "start_date": "2026-09-01",
        "end_date": "2026-09-15"
    }, headers=headers)
    
    assert resp.status_code == 200
    data = resp.get_json()
    assert "Berhasil menyimpan 5 berita baru" in data['message']
    mock_scrape.assert_called_once()
