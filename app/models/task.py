from app import db
from datetime import date



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
        
        nested_dict = {"task": task_as_dict}
        return nested_dict

    def mark_complete(self):
        today = date.today()
        self.completed_at = today

        if self.completed_at:
            self.is_complete = True