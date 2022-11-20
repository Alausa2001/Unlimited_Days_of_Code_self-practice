#!/usr/bin/python3
from flask_httpauth import HTTPBasicAuth
from flask import Flask, jsonify, abort, make_response, request, url_for
from uuid import uuid4
app = Flask(__name__)
auth = HTTPBasicAuth()


allowed = {'Alausa': "Feranmi", 'Ogede': 'Eniola'}
@auth.get_password
def auth(username):
    """authorizes a user"""
    for key, value in allowed.items():
        if key == username:
            return value


"""@auth.error_handler
def unauthorized():
    ""msg on failed authorization""
    return make_response(jsonify({'error': 'unauthorized'}))
"""

def uri(task):
    """improve web services for easy task access via uri"""
    new = {}
    for field in task:
        if field == 'id':
            new['uri'] = url_for('specific', tid=task['id'], _external=True)
        else:
            new[field] = task[field]
    return (new)


tasks = [
        {'id': int(uuid4()), 'task': 'Go to mosque'},
        {'id': int(uuid4()), 'task': 'Read Quran'}
        ]


@app.route('/todo/api/v1/tasks', methods=['GET'], strict_slashes=False)
@auth.login_required
def get():
    return jsonify({'tasks': [uri(task) for task in tasks]})


@app.route('/todo/api/v1/tasks/<int:tid>',
           methods=['GET'], strict_slashes=False)
def specific(tid):
    task = [task for task in tasks if task['id'] == tid]
    if task:
        return jsonify({'tasks': task})
    abort(404)


@app.route('/todo/api/v1/tasks', methods=['POST'], strict_slashes=False)
def create():
    if not request.json or 'task' not in request.json:
        abort(400)
    task = {'id': int(uuid4()), 'task': request.json['task']}
    tasks.append(task)
    return jsonify({'tasks': tasks}), 201


@app.route('/todo/api/v1/tasks/<int:tid>', methods=['PUT'],
           strict_slashes=False)
def update(tid):
    task = [task for task in tasks if task['id'] == tid]
    if not task:
        abort(404)
    if not request.json or 'task' not in request.json:
        abort(400)
    # task[0]['id'] = request.json.get('id')
    task[0]['task'] = request.json.get('task')
    # tasks.append(task)
    return jsonify('Your Update was succesful')


@app.route('/todo/api/v1/tasks/<int:tid>', methods=['DELETE'])
def delete_task(tid):
    task = [task for task in tasks if task['id'] == tid]
    if len(task) == 0:
        abort(404)
    tasks.remove(task[0])
    return jsonify({'result': True})


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'bad request'}), 400)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'not found'}), 404)


if __name__ == '__main__':
    app.run(debug=True)
