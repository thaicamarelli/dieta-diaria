from datetime import datetime,timezone
from database import db

class Meal(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(80),nullable=False)
    description = db.Column(db.String(80))
    datetime = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    on_diet = db.Column(db.Boolean())

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "datetime": self.datetime,
            "on_diet": self.on_diet
        }