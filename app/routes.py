from flask import Blueprint, jsonify, request, make_response, abort, abort, json
from app.models.task import Task
from app import db

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")


@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    new_task = Task(
        title=request_body["title"],
        description=request_body["description"]
        # id=request_body["id"],
        # is_complete=request_body["is_complete"]
        )

    db.session.add(new_task)
    db.session.commit()

    return make_response(jsonify(new_task.to_dict()), 201)


@tasks_bp.route("", methods=["GET"])
def get_tasks():
    tasks_response = []
    # task_query = Task.query
    sort_query = request.args.get("sort")

    if sort_query:
        ###working through descending order###
        # if sort_query == 'desc':
        #     tasks = Task.query.order_by(Task.-'title').all()
        tasks = Task.query.order_by(Task.title).all()
    else:
        tasks = Task.query.all()
    for task in tasks:
        tasks_response.append({
            "id":task.id,
            "title": task.title,
            "description": task.description,
            "is_complete": bool(task.is_complete)
        })

    # if sort_query:
    #     if sort_query == "asc":
    #         tasks_response = tasks_response.sort(key="title", reverse=False)

    return jsonify(tasks_response)

@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_task(task_id)

    return {
        "task": {
            "id" : task.id,
            "title": task.title,
            "description" : task.description,
            "is_complete": bool(task.is_complete)
        }
    }

def validate_task(task_id):
    try:
        task_id = int(task_id)
    except: 
        abort(make_response({"message":f"task {task_id} invalid"}, 400))
    task = Task.query.get(task_id)
    if not task:
        abort(make_response({"message": "id number not found"}, 404))
    
    return task
    


@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_task(task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return make_response(jsonify(task.to_dict()), 200)


@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_task(task_id)

    db.session.delete(task)
    db.session.commit()

    test_set = {"details: " f'Task {task_id} "{task.title}" successfully deleted'}
    json.dumps(list(test_set))
    return make_response(jsonify({"details: " f'Task {task_id} "{task.title}" successfully deleted'}))
    