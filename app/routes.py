from flask import Blueprint, jsonify, request, make_response
from app.models.task import Task
from app import db

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")


@tasks_bp.route("", methods=["POST"])
def create_task():

    request_body = request.get_json()
    new_task = Task(title=request_body["title"],
    description=request_body["description"])

    db.session.add(new_task)
    db.session.commit()
    
    return make_response(new_task.to_dict(), 201)


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
        # if task.is_complete == None:

    return jsonify(tasks_response)




    
# @tasks_bp.route("/<task_id>", methods=["GET"])
# def get_one_task(task_id):
#     try:
#         task_id = int(task_id)
#     except:
#         return {"message": "Please search with a valid number"}, 400
    
    
#     task_response = []
#     tasks = Task.query.all()

#     for task in tasks:
#         if task.id == task_id:
#             task_response.append({
#                 "id": task.id,
#                 "title": task.title,
#                 "description": task.description,
#                 "is_complete": task.is_complete
#             })
#             # if task.completed_at == None:
#             #     task_response.append({"is_complete" : False})
#     return jsonify(task_response)
#         # "id": task.id,
#         # "title": task.title,
#         # "description": task.description,
#         # "is_complete": task.is_complete,
#         # "completed_at": task.completed_at
#     # }