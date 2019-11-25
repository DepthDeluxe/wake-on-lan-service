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