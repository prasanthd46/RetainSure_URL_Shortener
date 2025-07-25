import pytest
from app.main import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    response = client.get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'
    assert data['service'] == 'URL Shortener API'
    
def test_shorten_valid_url(client):
    response = client.post('/api/shorten', json={'url': 'https://example.com'})
    data = response.get_json()

    assert response.status_code == 201
    assert 'short_code' in data
    assert 'short_url' in data

def test_shorten_missing_url_field(client):
    response = client.post('/api/shorten', json={})
    data = response.get_json()

    assert response.status_code == 400
    assert data['message'] == 'Missing url field'

def test_shorten_invalid_url(client):
    response = client.post('/api/shorten', json={'url': 'not-a-valid-url'})
    data = response.get_json()

    assert response.status_code == 400
    assert data['message'] == 'Invalid url'

def test_shorten_same_url_returns_same_code(client):
    url = 'https://example.com/same'
    res1 = client.post('/api/shorten', json={'url': url})
    res2 = client.post('/api/shorten', json={'url': url})

    code1 = res1.get_json()['short_code']
    code2 = res2.get_json()['short_code']

    assert code1 == code2

def test_redirect_valid_code(client):
    post_res = client.post('/api/shorten', json={'url': 'https://google.com'})
    short_code = post_res.get_json()['short_code']

    redirect_res = client.get(f'/{short_code}', follow_redirects=False)
    assert redirect_res.status_code == 302
    assert 'google.com' in redirect_res.headers['Location']

def test_redirect_invalid_code(client):
    response = client.get('/invalidcode123')
    data = response.get_json()

    assert response.status_code == 404
    assert data['message'] == 'Short code not found'
    
def test_stats_clicks_increment(client):
    url = 'https://yahoo.com'
    resp = client.post('/api/shorten', json={'url': url})
    code = resp.get_json()['short_code']
    for _ in range(3):
        client.get(f'/{code}', follow_redirects=False)
    stats_res = client.get(f'/api/stats/{code}')
    assert stats_res.get_json()['clicks'] == 3
    
def test_redirect_invalid_code(client):
    response = client.get('/invalidcode123')
    data = response.get_json()
    assert response.status_code == 404
    assert data['message'] == 'Short code not found'

def test_stats_invalid_code(client):
    response = client.get('/api/stats/invalidcode123')
    data = response.get_json()
    assert response.status_code == 404
    assert data['message'] == 'Short code not found'