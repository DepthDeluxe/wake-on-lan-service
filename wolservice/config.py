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
