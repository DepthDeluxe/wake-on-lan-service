import os
from logging.config import dictConfig

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
    }
})

from wolservice.server import app, db
from wolservice.backend import parse_config_file, NetworkManager
    

config = parse_config_file(os.environ.get('WOL_SERVICE_CONFIG', 'config.ini'))
app.config['NETWORK_MANAGER'] = NetworkManager()
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{config.database_path}'

db.metadata.create_all(db.engine)

if __name__ == '__main__':
    app.run()