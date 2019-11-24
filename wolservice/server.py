from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

import wolservice.backend as backend

app = Flask(__name__)
db = SQLAlchemy(app)

class WolEntity(db.Model):
    name = db.Column(db.String, primary_key=True)
    mac_address = db.Column(db.String)
    ip_address = db.Column(db.String)

    def __repr__(self):
        return f'WolEntity(name={name},mac_address={mac_address},ip_address={ip_address})'

    def to_json(self):
        return {
            'name': self.name,
            'mac_address': self.mac_address,
            'ip_address': self.ip_address
        }

@app.route('/')
def list_targets():
    items = db.session.query(WolEntity).all()
    return jsonify([item.to_json() for item in items])

@app.route('/', methods=['POST'])
def create():
    try:
        name = request.json['name']
        # mac_address = request.json['mac_address']
        ip_address = request.json['ip_address']
    except KeyError as e:
        return jsonify({'error': e}), 400

    mac_address = lookup_mac_address(ip_address)
    if mac_address is None:
        return jsonify({'error': 'Unable to find mac address'}), 400

    if not backend.validate_mac(mac_address) or not backend.validate_ip(ip_address):
        return jsonify({'error': 'Bad Mac or IP Address'}), 400

    record = WolEntity(name=name,mac_address=mac_address,ip_address=ip_address)
    try:
        db.session.add(record)
        db.session.commit()
    except IntegrityError:
        return jsonify({'error': 'A record already exists'}), 403

    return jsonify(record.to_json()), 200

@app.route('/<name>')
def get_by_name(name):
    record = db.session.query(WolEntity).get(name)
    if record == None:
        return jsonify({'error': 'Not found'}), 404
    else:
        return jsonify(record.to_json()), 200


@app.route('/<name>/wakeup')
def name_wakeup_action(name):
    record = db.session.query(WolEntity).get(name)
    if record == None:
        return jsonify({'error': 'Not found'}), 404

    try:
        backup.wakeup_and_wait_for_response(record)
    except Exception:
        return jsonify({'error': 'Unable to wakeup host'}), 500

    return jsonify({'status': 'Successful!'}), 200