from app import db


class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    # Parent - One To Many

# Turn into Json
    def g_json(self):
        return {
            "id": self.id,
            "title": self.title
        }
    
    # def to_dict(self)
# "id": self.goal_id,