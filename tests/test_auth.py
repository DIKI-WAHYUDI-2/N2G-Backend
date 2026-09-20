import pytest

def test_login_success(client):
    response = client.post('/auth/login', json={
        "username": "testadmin",
        "password": "testpassword"
    })
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == "success"
    assert data['message'] == "Login Success"
    assert data['role'] == "ADMIN"
    
    # Check if cookies are set
    cookies = response.headers.getlist('Set-Cookie')
    assert any('access_token=' in cookie for cookie in cookies)
    assert any('refresh_token=' in cookie for cookie in cookies)

def test_login_failure_invalid_credentials(client):
    response = client.post('/auth/login', json={
        "username": "testadmin",
        "password": "wrongpassword"
    })
    
    assert response.status_code == 401
    data = response.get_json()
    assert data['status'] == "error"
    assert "Username atau Password Salah" in data['message']

def test_access_protected_route_without_token(client):
    # /auth/me is protected
    response = client.get('/auth/me')
    assert response.status_code == 401
    data = response.get_json()
    assert "Unauthorized" in data['message']

def test_logout(client):
    # First login to get the cookies
    response = client.post('/auth/login', json={
        "username": "testadmin",
        "password": "testpassword"
    })
    
    # Send logout request, Flask test client handles cookies automatically!
    logout_response = client.post('/auth/logout')
    
    assert logout_response.status_code == 200
    data = logout_response.get_json()
    assert data['status'] == "success"
    assert data['message'] == "Logout Success"
    
    # Check if a protected route returns unauthorized because token was blacklisted/unset
    protected_response = client.get('/auth/me')
    assert protected_response.status_code == 401

def test_refresh_token(client):
    # First login
    client.post('/auth/login', json={
        "username": "testadmin",
        "password": "testpassword"
    })
    
    # Refresh token
    refresh_response = client.post('/auth/refresh-token')
    
    assert refresh_response.status_code == 200
    data = refresh_response.get_json()
    assert data['status'] == "success"
    assert data['message'] == "Refresh Success"
    
    cookies = refresh_response.headers.getlist('Set-Cookie')
    assert any('access_token=' in cookie for cookie in cookies)

