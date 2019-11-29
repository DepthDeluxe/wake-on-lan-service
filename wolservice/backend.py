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
    if address is None:
        return False

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


class NetworkManager:
    def get_mac_address(self, name: str) -> str:
        mac = getmac.get_mac_address(hostname=name)
        if mac is None:
            mac = getmac.get_mac_address(ip=name)

        if mac is None:
            raise ConnectionError(f"Cannot find device with name {name} on the network, please make sure it is awake.")

        return mac

    def ping(self, hostname: str, num_pings:int=3, timeout:int=15) -> bool:
        # wait for ping
        process = subprocess.Popen(['ping', '-c', str(num_pings), hostname], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            returncode = process.wait(timeout)
            if returncode != 0:
                raise ConnectionError(f'Unable to establish connection to host {hostname}, stdout={process.stdout.read()}, stderr={process.stderr.read()}')
        except subprocess.TimeoutExpired:
            process.kill()
            raise TimeoutError(f'Unable to wakeup host {hostname} in time')

        return True

    def wakeup(self, hostname: str, mac: str, timeout:int=None) -> None:
        wakeonlan.send_magic_packet(mac)

        if timeout is None:
            self.ping(hostname)
        else:
            self.ping(hostname, timeout=timeout)