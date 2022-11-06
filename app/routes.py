from flask import Blueprint, jsonify, request, make_response, abort
from app.models.task import Task
from app import db

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")


@tasks_bp.route("", methods=["POST"])
def create_task():
    response = request.get("http://127.0.0.1:5000/tasks")
    request_body = request.get_json()
    new_task = Task(title=request_body["title"],
    description=request_body["description"],
    completed_at=request_body["completed_at"],
    is_complete = request_body["is_complete"])

    if new_task.completed_at == "null":
        new_task.is_complete = False
        # new_task.completed_at = None

    db.session.add(new_task)
    db.session.commit()
    

    # return response.status_code, response.status_message, make_response(jsonify(new_task.to_dict), 201)
    return make_response(jsonify(new_task.to_dict), 201)

@tasks_bp.route("", methods=["GET"])
def get_tasks():
    tasks = Task.query.all()
    tasks_response = []
    for task in tasks:
        tasks_response.append({
            "id":task.id,
            "title": task.title,
            "description": task.description,
            "is_complete": task.is_complete
        })
    return jsonify(tasks_response)

'''
Added in please check over: Goal Update & Delete for Wave 1
'''
def validate_task(task_id):
    tasks = Task.query.all()
    try:
        task_id = int(task_id)
    except: 
        abort(make_response({"message":f"task {task_id} invalid"}, 400))

    for task in tasks:
        if task.id == task_id:
            return task_id
    
    abort(make_response({"message": f"task {task_id} not found"}, 404))


@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_task(task_id)
    
    
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return make_response(f"Task # {task.id} successfully updated", 200)


@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_task(task_id)

    db.session.delete(task)
    db.session.commit()

    return make_response(f"Task #{task_id} successfully deleted")

    
    
