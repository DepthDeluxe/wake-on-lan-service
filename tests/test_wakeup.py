import pytest
import wakeonlan
from unittest.mock import MagicMock
from dataclasses import dataclass

import wolservice.backend as backend

@dataclass
class SampleEntity:
    mac_address: str
    ip_address: str

@pytest.fixture
def mocked_send_magic_packet(monkeypatch):
    mock_smp = MagicMock()
    monkeypatch.setattr(wakeonlan, 'send_magic_packet', mock_smp)

    return mock_smp

def test_send_magic_packet_called(monkeypatch, mocked_send_magic_packet):
    def mock_ping(ip, timeout):
        pass

    monkeypatch.setattr(backend, 'ping', mock_ping)
    backend.wakeup_and_wait_for_response(SampleEntity('00:00:00:00:00:00', '1.2.3.4'), 10)

    assert mocked_send_magic_packet.called


def test_wakeup_timeout(monkeypatch, mocked_send_magic_packet):
    def mock_ping(ip, timeout):
        raise TimeoutError()

    monkeypatch.setattr(backend, 'ping', mock_ping)

    try:
        backend.wakeup_and_wait_for_response(SampleEntity('00:00:00:00:00:00', '1.2.3.4'), 10)
        assert False
    except TimeoutError:
        pass

def test_wakeup_connection_error(monkeypatch, mocked_send_magic_packet):
    def mock_ping(ip, timeout):
        raise ConnectionError()

    monkeypatch.setattr(backend, 'ping', mock_ping)

    try:
        backend.wakeup_and_wait_for_response(SampleEntity('00:00:00:00:00:00', '1.2.3.4'), 10)
        assert False
    except ConnectionError:
        pass

@pytest.mark.skip(reason='Cannot run inside CircleCI since container doens\'t have permission to run ping')
def test_ping_localhost():
    assert backend.ping('localhost', num_pings=3, timeout=5)

    try:
        backend.ping('localhost', num_pings=100, timeout=5)
        assert False
    except TimeoutError:
        pass