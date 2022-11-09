from flask import Blueprint, jsonify, request, make_response, abort, abort
from app.models.goal import Goal
from app import db


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

    # return make_response(jsonify(new_goal.g_json()), 201)
    
    # return make_response(jsonify({'goal': new_goal.g_jason()}), 201)


# def create_goal():
#     request_body = request.get_json()
#     try:
#         request_body["title"]
#     except:
#         abort(make_response({"details":"Invalid data"}, 400))
#     try:
#         request_body["description"]
#     except:
#         abort(make_response({"details":"Invalid data"}, 400))

#     new_goal = Goal(
#         title=request_body["title"],
#         description=request_body["description"]
#         )

#     db.session.add(new_goal)
#     db.session.commit()

#     return make_response(jsonify(new_goal.g_jason()), 201)


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

    # return jsonify({"goal": goal.g_json()}), 200


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
