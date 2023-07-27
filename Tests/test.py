import pytest
import requests

@pytest.fixture
def api_url():
    return 'https://mbcreditmodelapi.azurewebsites.net/predict'

def test_prediction_accept(api_url):
    data = {'data':100001}
    response = requests.post(api_url, json=data)
    assert response.status_code == 200
    assert 'prediction' in response.json()
    prediction = response.json()['gauge']
    assert prediction == 'Credit pouvant être accepté'

def test_prediction_accept(api_url):
    data = {'data': 100005}
    response = requests.post(api_url, json=data)
    assert response.status_code == 200
    assert 'prediction' in response.json()
    prediction = response.json()['gauge']
    assert prediction == 'Credit non accepté'
