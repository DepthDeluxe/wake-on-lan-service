from dataclasses import dataclass

import pytest
import getmac

from wolservice.network import validate_mac, validate_ip, NetworkManager

def test_ip():
    assert validate_ip('1.2.3.4') == True

    assert validate_ip('1.2.3:4') == False
    assert validate_ip('1.2.3.4.5') == False
    assert validate_ip('3....23.3.3.3..2.2..3') == False
    assert validate_ip('a.b.c.d') == False

def test_mac():
    assert validate_mac('00:00:00:00:00:00') == True
    assert validate_mac('12:34:56:78:90:AB') == True

    assert validate_mac('00:00:00:00:00:FFF') == False
    assert validate_mac('00.00.00.00.00.FF') == False
    assert validate_mac('00.00.00.00.00.XX') == False
    assert validate_mac('00:00:00:00:00:FF:00') == False

@pytest.fixture()
def network_manager():
    return NetworkManager()

@pytest.mark.skip(reason='Cannot run ping in CircleCI instance')
def test_network_manager_successful_ping(network_manager):
    result = network_manager.ping('localhost', num_pings=1, timeout=10)

    assert result

@pytest.mark.skip(reason='Cannot run ping in CircleCI instance')
def test_network_manager_connection_error(network_manager):
    try:
        network_manager.ping('??__??__Unknown__HOST__??')
        assert False
    except ConnectionError:
        pass

@pytest.mark.skip(reason='Cannot run ping in CircleCI instance')
def test_network_manager_timeout(network_manager):
    try:
        network_manager.ping('localhost', timeout=0, num_pings=3)
        assert False
    except TimeoutError:
        pass
