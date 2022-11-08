from flask import Blueprint, jsonify, request, make_response, abort, abort
from app.models.goal import Goal
from app import db


goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")


@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    try:
        request_body["title"]
    except:
        abort(make_response({"details":"Invalid data"}, 400))
    try:
        request_body["description"]
    except:
        abort(make_response({"details":"Invalid data"}, 400))

    new_goal = Goal(
        title=request_body["title"],
        description=request_body["description"]
        )

    db.session.add(new_goal)
    db.session.commit()

    return make_response(jsonify(new_goal.to_dict()), 201)


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
            "description": goal.description,
            "is_complete": bool(goal.is_complete)
        })

    return jsonify(goals_response)

@goals_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    goal = validate_goal(goal_id)

    return {
        "goal": {
            "id" : goal.id,
            "title": goal.title,
            "description" : goal.description,
            "is_complete": bool(goal.is_complete)
        }
    }

def validate_goal(goal_id):
    try:
        goal_id = int(goal_id)
    except: 
        abort(make_response({"message":f"goal {goal_id} invalid"}, 400))
    goal = Goal.query.get(goal_id)
    if not goal:
        abort(make_response({"message": "id number not found"}, 404))
    
    return goal
    


@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_goal(goal_id)
    request_body = request.get_json()

    goal.title = request_body["title"]
    goal.description = request_body["description"]

    db.session.commit()

    return make_response(jsonify(goal.to_dict()), 200)


@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_goal(goal_id)

    db.session.delete(goal)
    db.session.commit()

    return {
        "details": f'Goal {goal.id} "{goal.title}" successfully deleted'
    }
