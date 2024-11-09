from datetime import datetime,timezone
from database import db
from models.user import User
from sqlalchemy.orm import relationship,validates

class Meal(db.Model):
    __tablename__ = 'meals'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(80),nullable=False)
    description = db.Column(db.String(80))
    datetime = db.Column(db.DateTime, default=datetime.now(timezone.utc),nullable=False)
    on_diet = db.Column(db.Boolean,nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)

    user = relationship('User',back_populates='meal')

    @validates('name','datetime','on_diet')
    def validate_fields(self,key,value):
        if key == 'name':
            if not value or not isinstance(value, str) or len(value) < 1:
                raise ValueError("Nome da refeição deve ser uma string não vazia.")
        elif key == 'on_diet':
            if not isinstance(value, bool):
                raise ValueError("Campo on_diet deve ser booleano não vazio.")
        elif key == 'datetime':
            if not value or not isinstance(value, datetime):
                raise ValueError("Data e hora da refeição deve ser um datetime não vazio .")
        return value

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "datetime": self.datetime,
            "on_diet": self.on_diet
        }
    