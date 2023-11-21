import list_groups
import subprocess
import grp

from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route('/')
def index():
    return 'Hello World'


@app.route('/<name>')
def print_name(name):
    return 'Hi, {}'.format(name)


@app.route('/api/items', methods=['GET'])
def get_items():
    items = [{"name": "Item1", "price": 10}, {"name": "Item2", "price": 15}]  # Example data
    return jsonify(items)


@app.route('/api/items', methods=['POST'])
def add_item():
    new_item = request.json  # Get data sent by client
    # Add logic to save this item to your database or data structure
    return jsonify(new_item), 201  # Returning the created item with a 201 Created status


@app.route('/logs', methods=['GET'])
def get_logs():
    output = subprocess.check_output(['/home/chase/PycharmProjects/11.14.23.API/scripts/list_logs.sh'])
    return jsonify(output.decode().splitlines())


@app.route('/groups', methods=['GET'])
def get_groups():
    groups = list_groups.list_groups()
    return jsonify(groups)


@app.route('/primarygroup', methods=['GET'])
def get_primary_group():
    username = request.args.get('user')
    if not username:
        return jsonify({'error': 'No username provided'}), 400
    try:
        output = subprocess.check_output(['/home/chase/PycharmProjects/11.14.23.API/scripts/get_primary_group.sh', username])
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
    app.run(debug=True)
