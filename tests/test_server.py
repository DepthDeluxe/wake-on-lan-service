from threading import Thread
from unittest.mock import MagicMock
from dataclasses import dataclass
from flask_sqlalchemy import SQLAlchemy

import json
import pytest

from wolservice.network import NetworkManager
from wolservice.server import app, db, WolEntity

@pytest.fixture
def network_manager():
    return NetworkManager()

@pytest.fixture
def database():
    db.drop_all()
    db.metadata.create_all(db.engine)

    return db

@pytest.fixture
def client(database, network_manager):
    app.config['NETWORK_MANAGER'] = network_manager
    app.network_manager = network_manager

    with app.test_client() as client:
        yield client

def test_get_all_with_no_records_yields_empty_response(client):
    response = client.get('/')

    assert response.status_code == 200
    assert len(to_json(response)) == 0

def test_post_new(network_manager, client):
    network_manager.get_mac_address = MagicMock(return_value='00:01:02:03:04:05')

    response = client.put('/router.localhost.com')

    assert response.status_code == 200
    assert response.json['hostname'] == 'router.localhost.com'
    assert response.json['mac_address'] == '00:01:02:03:04:05'
    
    record = db.session.query(WolEntity).get('router.localhost.com')
    assert record.hostname == 'router.localhost.com'
    assert record.mac_address == '00:01:02:03:04:05'

def test_get_all(database, client):
    first_entity = WolEntity(hostname='A', mac_address='00:00:00:00:00:00')
    database.session.add(first_entity)
    second_entity = WolEntity(hostname='B', mac_address='00:00:00:00:00:01')
    database.session.add(second_entity)
    database.session.commit()

    response = client.get()

    assert response.status_code == 200
    assert len(response.json) == 2
    assert first_entity.to_json() in response.json
    assert second_entity.to_json() in response.json


def test_get(database, client):
    entity = WolEntity(hostname='router.localhost.com', mac_address='01:02:03:04:05:06')
    database.session.add(entity)
    database.session.commit()

    response = client.get('/router.localhost.com')

    assert response.status_code == 200
    assert response.json['hostname'] == 'router.localhost.com'
    assert response.json['mac_address'] == '01:02:03:04:05:06'

def test_get_missing_record_returns_404(client):
    response = client.get('/A')

    assert response.status_code == 404

def test_wakeup_success(database, client, network_manager):
    entity = WolEntity(hostname='router.localhost.com', mac_address='01:02:03:04:05:06')
    database.session.add(entity)
    database.session.commit()

    network_manager.wakeup = MagicMock(return_value=None)

    response = client.get('/router.localhost.com/wakeup')

    assert response.status_code == 200
    network_manager.wakeup.assert_called_once_with('router.localhost.com', '01:02:03:04:05:06')

def test_wakeup_failure(database, client, network_manager):
    entity = WolEntity(hostname='router.localhost.com', mac_address='01:02:03:04:05:06')
    database.session.add(entity)
    database.session.commit()

    network_manager.wakeup = MagicMock(side_effect=TimeoutError('MY_ERROR'))

    response = client.get('/router.localhost.com/wakeup')

    assert response.status_code == 500
    assert to_json(response)['error'] == 'MY_ERROR'

def test_delete(database, client):
    entity = WolEntity(hostname='router.localhost.com', mac_address='01:02:03:04:05:06')
    database.session.add(entity)
    database.session.commit()

    response = client.delete('/router.localhost.com')

    assert response.status_code == 200
    record = database.session.query(WolEntity).get('router.localhost.com')
    assert record is None


def to_json(response):
    return json.loads(response.data.decode('utf-8'))


def test_wol_entity_equality():
    first_entity = WolEntity(hostname='A', mac_address='00:00:00:00:00:00')
    second_entity = WolEntity(hostname='A', mac_address='00:00:00:00:00:00')

    assert first_entity == second_entity
    assert second_entity == first_entity

def test_wol_entity_repr():
    mac_address = '10:11:12:11:10:09'
    hostname = 'my-local-host'
    entity = WolEntity(mac_address=mac_address, hostname=hostname)

    repr_ = entity.__repr__()

    assert mac_address in repr_
    assert hostname in repr_