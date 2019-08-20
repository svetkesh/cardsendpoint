#!flask/bin/python
from flask import Flask, jsonify, request, make_response, abort
try:
    from .calculator import calculate
except ImportError:
    from calculator import calculate  # fall back for running in pycharm
import logging
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()

app = Flask(__name__)

logging.basicConfig(filename="app.log", level=logging.DEBUG)


@auth.get_password
def get_password(username):
    if username == 'poker':
        return 'poker'
    return None


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/')
def index():
    return "It is poker calculator!"


@app.route('/data', methods=['POST'])
def add():
    app.logger.info("in post /data")
    data = request.get_json()
    app.logger.info(f"data:{data}")
    app.logger.info(f"data:{jsonify(data)}")
    app.logger.info(f"data:{request}")
    # return jsonify({'sum': data['x'] + data['y']})
    return str(data)


# simple test auth
@app.route('/api/v1.0/calculate/<hand>', methods=['GET'])
@auth.login_required
def calculate_hand(hand):
    app.logger.info(type(hand), hand)
    # return jsonify({'tasks': tasks})
    return jsonify(calculate(hand))


@app.route('/api/v1.0/hands', methods=['POST'])
def calculate_hands():

    app.logger.info(request.get_json())

    if not request.json: # or not 'player' in request.json:
        abort(400)
    # hand = {
    #     'player': request.json['player'],
    #     'hand': request.json['hand'],
    #     # 'hand': request.json.get('hand', ""),
    #     # 'done': False
    # }

    hand = request.json['hand']
    app.logger.info(hand)

    # return jsonify({'hand': hand}), 201
    # return jsonify({'hand': calculate(hand)}), 201
    return jsonify({'hand': calculate(hand)}), 201


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5005', debug=True)
