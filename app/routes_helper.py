from flask import jsonify, abort, make_response

def get_record_by_id(cls, id):
    try:
        id = int(id)
    except ValueError:
        abort(make_response(jsonify({"message": f"Invalid id {id}"}), 400))