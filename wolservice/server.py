from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

import wolservice.backend as backend

app = Flask(__name__)
db = SQLAlchemy(app)

class WolEntity(db.Model):
    hostname = db.Column(db.String, primary_key=True)
    mac_address = db.Column(db.String)

    def __repr__(self):
        return f'WolEntity(name={name},mac_address={mac_address},hostname={hostname})'

    def to_json(self):
        return {
            'hostname': self.hostname,
            'mac_address': self.mac_address
        }

@app.route('/')
def list_targets():
    items = db.session.query(WolEntity).all()
    return jsonify([item.to_json() for item in items])

@app.route('/', methods=['POST'])
def create():
    try:
        hostname = request.json['hostname']
        app.logger.info(f'hostname is {hostname}')
    except KeyError as e:
        raise RestException(e, 400)

    network_manager = _get_network_manager();

    try:
        mac_address = network_manager.get_mac_address(hostname)
        app.logger.info(f'found mac addres {mac_address}')
    except ConnectionError as e:
        app.logger.error('Unable to get mac address for hostname')
        raise RestException(e, 400)

    if not backend.validate_mac(mac_address):
        raise RestException('Supplied mac addresss is in improper format', 400)

    record = WolEntity(hostname=hostname,mac_address=mac_address)
    try:
        db.session.add(record)
        db.session.commit()
    except IntegrityError:
        raise ConflictRestException()

    return jsonify(record.to_json()), 200

@app.route('/<hostname>')
def get_by_name(hostname):
    record = get_or_throw_if_missing(hostname)
    return jsonify(record.to_json()), 200

@app.route('/<hostname>', methods=['DELETE'])
def delete_by_name(hostname):
    record = get_or_throw_if_missing(hostname)
    db.session.delete(record)
    db.session.commit()

    return jsonify(record.to_json()), 200

@app.route('/<hostname>/wakeup')
def name_wakeup_action(hostname):
    record = get_or_throw_if_missing(hostname)

    network_manager = _get_network_manager()
    try:
        network_manager.wakeup(hostname, record.mac_address)
    except Exception as e:
        raise RestException(e, 500)

    return jsonify({'status': 'Successful!'}), 200

def get_or_throw_if_missing(hostname):
    record = db.session.query(WolEntity).get(hostname)
    if record == None:
        raise NotFoundRestException()

    return record

def _get_network_manager() -> backend.NetworkManager:
    return app.config['NETWORK_MANAGER']


class RestException(Exception):
    def __init__(self, message, code):
        self.message = message
        self.code = code

class ConflictRestException(RestException):
    def __init__(self):
        super().__init__('Conflict', 409)

class NotFoundRestException(RestException):
    def __init__(self):
        super().__init__('Not Found', 404)

@app.errorhandler(RestException)
def handle_rest_exception(error):
    return jsonify({'error': str(error.message)}), error.code

@app.errorhandler(Exception)
def handle_general_exception(error):
    return jsonify({'error': f'Hit uncaught exception: {error}'}, 500)