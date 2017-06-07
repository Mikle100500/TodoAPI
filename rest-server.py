#!flask/bin/python

from flask import Flask, jsonify, abort, request, make_response, url_for
from flask_httpauth import HTTPBasicAuth
  

app = Flask(__name__, static_url_path = "")
auth = HTTPBasicAuth()

users = {
	"john": "malkovich",
	"mikhail": "pavlenko",
	"julia": "iluhina",
	"jakiv": "kramarenko"
}

@auth.get_password
def get_password(username): 
    if username in users: 
        return users.get(username)
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify( { 'error': 'Unauthorized access, so hold your horses, cowboy' } ), 403)

@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify( { 'error': 'Bad request' } ), 400)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found and never gonna be' } ), 404)

tasks = [
    {
        'id': '01',
        'title': u'Call fire station',
        'description': u'Call in case of fire or natural disaster',
        'done': False
    },
    {
        'id': '02',
        'title': u'Call police',
        'description': u'Call in case of crime',
        'done': False
    },
	{
        'id': '03',
        'title': u'Call emergency',
        'description': u'Call in case you are injured',
        'done': False
    }
]

def make_public_task(task):
    new_task = {}
    for field in task:  
        if field == 'id':
            new_task['uri'] = url_for('get_task', task_id = task['id'], _external = True)
        else:
            new_task[field] = task[field]
    return new_task

@app.route('/todo/api/tasks', methods = ['GET'])
@auth.login_required
def get_tasks():
    return jsonify( { 'tasks': map(make_public_task, tasks) } )
 

@app.route('/todo/api/tasks/<string:task_id>', methods = ['GET'])
@auth.login_required
def get_task(task_id):
    task = filter(lambda t: t['id'] == task_id, tasks)
    if len(task) == 0:
        abort(404)
    return jsonify( { 'task': make_public_task(task[0]) } )

@app.route('/todo/api/v1.0/tasks/<string:task_id>', methods = ['POST'])
@auth.login_required
def create_task(task_id):
    if not request.json or not 'title' in request.json:
        abort(400)
    task = {
        'id': task_id,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    tasks.append(task)
    return jsonify( { 'task': make_public_task(task) } ), 201

@app.route('/todo/api/tasks/<string:task_id>', methods = ['PUT'])
@auth.login_required
def update_task(task_id):
    task = filter(lambda t: t['id'] == task_id, tasks)
    if len(task) == 0:
        abort(404)
    elif not request.json:
        abort(400)
    elif 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    elif 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400)
    elif 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
	task[0]['title'] = request.json.get('title', task[0]['title'])
	task[0]['description'] = request.json.get('description', task[0]['description'])
	task[0]['done'] = request.json.get('done', task[0]['done'])
	return jsonify( { 'task': make_public_task(task[0]) } )

@app.route('/todo/api/tasks/<string:task_id>', methods = ['DELETE'])
@auth.login_required
def delete_task(task_id):
    task = filter(lambda t: t['id'] == task_id, tasks)
    if len(task) == 0:
        abort(404)
    tasks.remove(task[0])
    return jsonify( { 'result': True } )

if __name__ == '__main__':
    app.run(debug = True)
