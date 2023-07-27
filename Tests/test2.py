import pytest
import requests

@pytest.fixture
def api_url():
    return 'https://mbcreditmodelapi.azurewebsites.net/update'

def test_update_accept(api_url):
    data = {'data': {'client_id': 425433, 'CODE_GENDER': 'F'}}
    response = requests.post(api_url, json=data)
    assert response.status_code == 200
    assert 'prediction' in response.json()
    prediction = response.json()['gauge']
    assert prediction == 'Credit accepté'

def test_update_accept(api_url):
    data = {'data': {'client_id': 174590, 'CODE_GENDER': 'F'}}
    response = requests.post(api_url, json=data)
    assert response.status_code == 200
    assert 'prediction' in response.json()
    prediction = response.json()['gauge']
    assert prediction == 'Credit refusé'
