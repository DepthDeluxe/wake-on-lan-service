from wolservice.server import app, db
from wolservice.backend import parse_config_file

config = parse_config_file('config.ini')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{config.database_path}'

db.metadata.create_all(db.engine)