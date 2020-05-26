from flask_sqlalchemy import SQLAlchemy

from .app import app

db = SQLAlchemy(app)

class WolEntity(db.Model):
    hostname = db.Column(db.String, primary_key=True)
    mac_address = db.Column(db.String)

    def __repr__(self):
        return f'WolEntity(hostname={self.hostname},mac_address={self.mac_address})'

    def to_json(self):
        return {
            'hostname': self.hostname,
            'mac_address': self.mac_address
        }

    def __eq__(self, obj):
        if not isinstance(obj, WolEntity):
            return False
        
        return self.hostname == obj.hostname and \
            self.mac_address == obj.mac_address
