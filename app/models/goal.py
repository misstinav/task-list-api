from app import db


class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    tasks = db.relationship("Task", back_populates='goal', lazy=True)

    def g_json(self):
        return {
            "id": self.id,
            "title": self.title
        }