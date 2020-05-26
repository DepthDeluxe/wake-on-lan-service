import os
import logging
from logging.config import dictConfig

from wolservice.app import app
from wolservice.network import NetworkManager
from wolservice.config import parse_config_file, load_default_configuration, load_config_from_file
from wolservice.models import db

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
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    db.metadata.create_all(db.engine)
    app.run(debug=True)