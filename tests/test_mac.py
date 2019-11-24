from dataclasses import dataclass

import pytest
import getmac

from wolservice.backend import validate_mac, validate_ip, wakeup_and_wait_for_response

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

def test_wakeup():
    @dataclass
    class SampleEntity:
        name: str
        ip_address: str
        mac_address: str

    entity = SampleEntity(name='router', ip_address='10.0.0.1', mac_address=getmac.get_mac_address(ip='10.0.0.1'))
    wakeup_and_wait_for_response(entity, 10)

    bad_entity = SampleEntity(name='router', ip_address='1.2.3.4', mac_address=getmac.get_mac_address(ip='10.0.0.1'))
    try:
        wakeup_and_wait_for_response(entity, 5)
        assert False
    except Exception:
        pass