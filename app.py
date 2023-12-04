import hmac
import subprocess
from datetime import timedelta

from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, jwt_required, \
    get_jwt_identity

import list_groups

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'change-this-secret'  #  TO DO: import secrets and create env variable in /etc/apache2/myapp.conf,
jwt = JWTManager(app)

# fake DB for testing
users_db = {
    "user1": {"username": "user1", "password": "password1"},
    "user2": {"username": "user2", "password": "password2"},
}


# authenticate user
def authenticate(username, password):
    user = users_db.get(username, None)
    if user and hmac.compare_digest(user['password'], password):
        return user


@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    user = authenticate(username, password)
    if not user:
        return jsonify({"msg": "Bad username or password"}), 401

    # short expiry for access token
    access_expires = timedelta(days=1)
    access_token = create_access_token(identity=username, expires_delta=access_expires)

    # long expiry for refresh token
    refresh_expires = timedelta(days=30)
    refresh_token = create_refresh_token(identity=username, expires_delta=refresh_expires)

    # menu of routes for user
    routes_info = {
        '/protected': 'Access to protected page',
        '/api/items': 'Get or add items',
        '/logs': 'View logs',
        '/groups': 'View groups',
        '/primarygroup': 'Get primary group for a user',
        '/token/refresh': 'Refresh your access token'
    }

    return jsonify(access_token=access_token, refresh_token=refresh_token, msg="Login successful", routes=routes_info)


@app.route('/token/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    new_token = create_access_token(identity=current_user, expires_delta=timedelta(days=30))
    return jsonify({'access_token': new_token})


@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    return jsonify({"msg": "Access to protected page granted"})


@app.route('/api/items', methods=['GET'])
@jwt_required()
def get_items():
    items = [{"employee": "john", "contracts": 10}, {"employee": "jane", "contracts": 20}]  # example
    return jsonify(items)


@app.route('/api/items', methods=['POST'])
@jwt_required()
def add_item():
    new_item = request.json
    # put db logic here
    return jsonify(new_item), 201  # return created status, 201?


@app.route('/logs', methods=['GET'])
@jwt_required()
def get_logs():
    output = subprocess.check_output(['/home/chase/PycharmProjects/11.14.23.API/scripts/list_logs.sh'])
    return jsonify(output.decode().splitlines())


@app.route('/groups', methods=['GET'])
@jwt_required()
def get_groups():
    groups = list_groups.list_groups()
    return jsonify(groups)


@app.route('/primarygroup', methods=['GET'])
@jwt_required()
def get_primary_group():
    username = request.args.get('user')
    if not username:
        return jsonify({'error': 'No username provided'}), 400
    try:
        output = subprocess.check_output(
            ['/home/chase/PycharmProjects/11.14.23.API/scripts/get_primary_group.sh', username])
        return jsonify({'primary_group': output.decode().strip()})
    except subprocess.CalledProcessError as e:
        return jsonify({'error': 'Error getting primary group'}), 500


@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404


def application(environ, start_response):
    status = '200 OK'
    output = b'Hello World!'

    response_headers = [('Content-type', 'text/plain'), ('Content-Length', str(len(output)))]
    start_response(status, response_headers)

    return [output]


if __name__ == '__main__':
    app.run(debug=True)     # if w/ flask, else w/ apache
else:
    application = app
