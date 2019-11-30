from threading import Thread
from unittest.mock import MagicMock
from dataclasses import dataclass

import json
import pytest

from wolservice.backend import NetworkManager
from wolservice.server import app, db, WolEntity

@pytest.fixture
def network_manager():
    return NetworkManager()

@pytest.fixture
def client(network_manager):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['NETWORK_MANAGER'] = network_manager
    app.network_manager = network_manager

    db.metadata.create_all(db.engine)

    with app.test_client() as client:
        yield client


def test_get_with_nothing(client):
    response = client.get('/')

    assert response.status_code == 200
    assert len(to_json(response)) == 0

def test_post_new(network_manager, client):
    network_manager.get_mac_address = MagicMock(return_value='00:01:02:03:04:05')

    response = client.post(data=json.dumps(dict(hostname='router.localhost.com')), content_type='application/json')

    print(response.data)

    assert response.status_code == 200
    response_json = to_json(response)
    assert response_json['hostname'] == 'router.localhost.com'
    assert response_json['mac_address'] == '00:01:02:03:04:05'

def test_newly_created_element_appears_in_get_all(client):
    response = client.get()

    assert response.status_code == 200
    response_json = to_json(response)
    assert len(response_json) == 1
    assert response_json[0]['hostname'] == 'router.localhost.com'

def test_newly_create_element_appears_in_get_by_name(client):
    response = client.get('/router.localhost.com')

    assert response.status_code == 200
    response_json = to_json(response)
    assert response_json['hostname'] == 'router.localhost.com'
    assert response_json['mac_address'] == '00:01:02:03:04:05'

def test_wakeup_success(client, network_manager):
    network_manager.wakeup = MagicMock(return_value=None)

    response = client.get('/router.localhost.com/wakeup')

    assert response.status_code == 200
    network_manager.wakeup.assert_called_once_with('router.localhost.com', '00:01:02:03:04:05')

def test_wakeup_failure(client, network_manager):
    network_manager.wakeup = MagicMock(side_effect=TimeoutError('MY_ERROR'))

    response = client.get('/router.localhost.com/wakeup')

    assert response.status_code == 500
    assert to_json(response)['error'] == 'MY_ERROR'

def test_delete(client):
    response = client.delete('/router.localhost.com')
    assert response.status_code == 200

    response = client.get('/router.localhost.com')
    assert response.status_code == 404

def to_json(response):
    return json.loads(response.data.decode('utf-8'))