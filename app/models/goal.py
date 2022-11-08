from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    # Parent - One To Many

# Turn into Json
    def g_json(self):
        return {
            "id": self.goal_id,
            "title": self.title
        }
    
    # def to_dict(self)
# "id": self.goal_id,