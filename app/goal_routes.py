from flask import Blueprint, jsonify, request, make_response, abort, abort
from app.models.goal import Goal
from app.models.task import Task
from app.routes_helper import *
from app import db
# from app.task_routes import validate_model


goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")


@goals_bp.route("/<id>", methods = ["GET"])
def get_all_goals(id):
    goal = validate_goal(id)

    return jsonify({"goal": {
        "id": goal.id,
        "title": goal.title
    }}), 200


@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()

    # guard clause
    if "title" not in request_body:
        return {"details": "Invalid data"}, 400
    new_goal = Goal(
        title=request_body['title']
        )
    
    db.session.add(new_goal)
    db.session.commit()
    
    return make_response(jsonify({'goal': new_goal.g_json()}), 201)

@goals_bp.route("", methods=["GET"])
def get_goals():
    goals_response = []
    sort_query = request.args.get("sort")

    if sort_query:
        if sort_query == 'desc':
            goals = Goal.query.order_by(Goal.title.desc())
        else:
            goals = Goal.query.order_by(Goal.title).all()
    else:
        goals = Goal.query.all()

    for goal in goals:
        goals_response.append({
            "id":goal.id,
            "title": goal.title,
        })

    return jsonify(goals_response)

@goals_bp.route("/<id>", methods=["GET"])
def get_one_goal(id):
    goal = validate_goal(id)

    return jsonify({
        "goal": {
            "id" : goal.id,
            "title": goal.title
        }
    }), 200 

def validate_goal(id):
    try:
        id = int(id)
    except: 
        return abort(make_response({"message" : f"goal {id} is invalid"}, 400))
    
    goal = Goal.query.get(id)
    
    if not goal:
        abort(make_response({"message": f"goal {id} not found"}, 404))
    
    return goal

@goals_bp.route("/<id>", methods=["PUT"])
def update_goal(id):
    goal = validate_goal(id)
    request_body = request.get_json()

    goal.title = request_body["title"]

    
    db.session.commit()

    return jsonify({"goal":goal.g_json()}), 200


@goals_bp.route("/<id>", methods=["DELETE"])
def delete_goal(id):
    goal = validate_goal(id)

    db.session.delete(goal)
    db.session.commit()

    return {
        "details": f'Goal {goal.id} "{goal.title}" successfully deleted'
    }

@goals_bp.route("/<id>/tasks", methods=["POST"])
def create_task_for_goal(id):
    request_body = request.get_json() #{"task_ids": [1,2,3]}
    id = validate_goal(id)
    task_goal_id_list = []
    tasks_to_connect = request_body["task_ids"]

    for task in tasks_to_connect:
        Task.query.filter(task).update(goal_id=id)
        task_goal_id_list.append(Task.query.filter_by(goal_id=id))

    return jsonify({
        "id": id,
        "task_ids": task_goal_id_list
        })
    












    # id = validate_goal(id)
    # goal = Goal.query.get(id)
    # tasks_to_connect = request_body["tasks_list"]

    # for task in tasks_to_connect:
    #     if not task.goal_id:
    #         Task.query.filter(task).update(goal_id=goal.id)

    # return jsonify({
    #     "id": id,
    #     "task_ids": tasks_to_connect 
    #     })













#     goal = get_record_by_id(Task, id)
#     tasks_ids_response = []

#     new_task = Task.from_dict(request_body)
#     # new_task.goal = goal
# # new_task = Task(
# #         title=request_body["title"],
# #         description=request_body["description"]


#     db.session.add(new_task)
#     db.session.commit()
    # for task in goal.tasks:
    #     tasks_ids_response.append(task.id)

    # return jsonify({
    #     "id": new_task.goal.id,
    #     # "task_ids": 
    #     })



# @goals_bp.route("/goals/<id>/tasks", methods=["GET"])
# def read_tasks(goal_id):
#     goal = validate_goal(Goal, goal_id)
#     tasks_response = []
#     # for goal in goal.tasks:
#     #     tasks_response.append(
#     #         {
#     #                 "id": goal.task.id,
#     #                 "goal_id": goal.task.goal_id,
#     #                 "title": goal.task.title,
#     #                 "description": goal.task.description,
#     #                 "is_complete": goal.task.is_complete
#     #         }
#     #     )

#     return jsonify({
#         "id": goal_id,
#         "title": goal.title,
#         "tasks": tasks_response
#     })