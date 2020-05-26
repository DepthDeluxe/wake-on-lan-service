from dataclasses import dataclass
import configparser
import os

from .network import NetworkManager

@dataclass
class Config:
    database_path: str

def parse_config_file(filename: str) -> Config:
    config = configparser.ConfigParser()
    config.read(filename)

    try:
        return Config(database_path=config['database']['path'])
    except KeyError as e:
        raise ValueError('Configuration is missing', e)

def load_default_configuration(app):
    app.config['NETWORK_MANAGER'] = NetworkManager()
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///:memory:'

def load_config_from_file(app, config=os.environ.get('WOL_SERVICE_CONFIG', 'config.ini')):
    config = parse_config_file(config)

    app.config['NETWORK_MANAGER'] = NetworkManager()
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{config.database_path}'
