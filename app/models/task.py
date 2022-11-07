from app import db
import json
from serpy import Serializer, IntField, StrField, MethodField, BoolField


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)
    is_complete = db.Column(db.Boolean)

    def to_dict(self):
        task_as_dict = {}
        task_as_dict["id"] = self.id
        task_as_dict["title"] = self.title
        task_as_dict["description"] = self.description
        task_as_dict["is_complete"] = bool(self.is_complete)
        # if not self.completed_at:
        #     task_as_dict["is_complete"] = False
        
        nested_dict = {"task": task_as_dict}
        return json.dumps(nested_dict)

# class TaskSerializer(Serializer):
#     id = IntField(required=True)
#     title = StrField(required=True)
#     description = StrField(required=True)
#     completed_at = MethodField('serializable_completed_at')
#     is_complete = BoolField(required=True)

#     def serialized_completed_at(self, task):
#         return task.completed_at.isoformat()
    