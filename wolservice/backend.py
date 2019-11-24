import getmac
import wakeonlan
import subprocess
from dataclasses import dataclass
import configparser

@dataclass
class Config:
    database_path: str

def parse_config_file(filename: str) -> Config:
    # todo: colin add config
    config = configparser.ConfigParser()
    config.read(filename)

    return Config(database_path=config['database']['path'])


# Valiates an IPv4 address
def validate_ip(address: str) -> bool:
    split = address.split('.')
    if len(split) != 4:
        return False
    for item in split:
        try:
            int(item)
        except ValueError:
            return False

    return True

# validates mac address
# example 4e:00:69:38:cd:05
def validate_mac(address: str) -> bool:
    split = address.split(':')
    if len(split) != 6:
        return False
    
    for pair in split:
        try:
            value = int('0x' + pair, 0)
        except ValueError:
            return False

        if value < 0 or value > 255:
            return False
    
    return True


def lookup_mac_address(ip_address: str) -> str:
    return getmac.get_mac_address(ip=ip_address)

def ping(ip_address: str, num_pings:int=3, timeout:int=15) -> bool:
    # wait for ping
    process = subprocess.Popen(['ping', '-c', str(num_pings), ip_address])
    try:
        returncode = process.wait(timeout)
        if returncode != 0:
            raise ConnectionError(f'Unable to establish connection to host {ip_address}')
    except subprocess.TimeoutExpired:
        process.kill()
        raise TimeoutError(f'Unable to wakeup host {ip_address} in time')

    return True

def wakeup_and_wait_for_response(entity, timeout=None):
    wakeonlan.send_magic_packet(entity.mac_address, ip_address=entity.ip_address)

    if timeout is None:
        ping(entity.ip_address)
    else:
        ping(entity.ip_address, timeout=timeout)