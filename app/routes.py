from flask import Blueprint, jsonify, request, make_response
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
